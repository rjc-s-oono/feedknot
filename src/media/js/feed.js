//+ フィード追加関連 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

// フィード検索開始 (Google findFeeds)
function searchFeed(searchTxt) {
    if (searchTxt.replace(/\s+$/, "") == "") {
        finishLoadingEffect();
        $(".feed_list_ul").empty();
        return;
    }

    if ( ! startLoadingEffect("Searching...")) {
        return;
    }
    if ( searchTxt.match(/^(http|https)\:\/\/.+/) ) {
        // 検索テキストがURLである為、そのデータを取得
        var feed = new google.feeds.Feed(searchTxt);
        feed.load(addFeedFromUrl);
    } else {
        // Google RSS検索
        google.feeds.findFeeds(searchTxt, dispFeed);
    }
}

// 取得結果 (Google Feed.load)
function addFeedFromUrl(result) {
    if (!result.error){
        //alert("title: " + result.feed.title);
        $("#searc-basic").val("");
        finishLoadingEffect();    // addFeed()内でもくるくる開始してるので先に終了させる
        addFeed(result.feed.link, result.feed.title, "");
    } else {
        alert("フィードの追加に失敗しました。正しいURLか検索キーワードを入力してください。。");
//        var errMsg = "feed情報取得でエラー:["+ result.error.code + ":" + result.error.message +"]";
//        alert(errMsg);
//        log.warn(errMsg);
        finishLoadingEffect();
    }
}

// 検索結果 (Google findFeeds)
function dispFeed(result) {
    if (!result.error){
        // エラーが発生していない場合の処理
        if (0 < result.entries.length) {
            $(".feed_list_ul").empty();

            for (var i = 0; i < result.entries.length; i++) {
                var title = result.entries[i].title;
                var link = result.entries[i].link;
                var contentSnippet = result.entries[i].contentSnippet;
                var url = result.entries[i].url;

	            var tag = "<li data-theme=\"c\" data-icon=\"plus\" class=\"feedLI" + i + "\">" +
	                          "<a onclick=\"addFeed('#url#', '#title#','feedLI" + i + "')\">" +
	                              "<div class=\"ui-feed-name\">#title#</div>" +
	                              "<div class=\"ui-feed-url\">#url#</div></a>" +
	                      "</li>";
                tag = tag.replace(/#url#/g, url);
                tag = tag.replace(/#title#/g, title);

                $(".feed_list_ul")
                    .attr("data-role","listview")
                    .append(tag);
            }
            $(".feed_list_ul")
                .listview().listview('refresh');
        }
    } else {
        var errMsg = "feed検索でエラー:["+result.query+"]";
        log.warn(errMsg);
    }
    finishLoadingEffect();
}

// タッチしたフィードをDBに追加
function addFeed(url, title, className) {
    if ( ! startLoadingEffect("Adding...")) {
        return;
    }

    $("form#feed_form #url").val(url);
    $("form#feed_form #title").val(title);
    $("form#feed_form #className").val(className);
    //alert("send feed." + $("form#feed_form #title").val());

    // フィードを追加
    $.ajax({
        type: "POST",
        url: $("form#feed_form").attr("action"),
        data: $("form#feed_form").serialize(),
        dataType: "json",
        success: function(data, status, xhr) {
            //alert("status:" + status);
            //alert("data:" + data);
            //alert("result:" + data.result);
            //alert($("#csrfmiddlewaretoken").val());
            //alert("title:" + data.title)
            if(data.result == 'error2') {
                alert("選択したフィードはすでに設定済です。");
            } else if (data == null || undefined == data.title || undefined == data.result) {
                alert("フィードの追加に失敗しました。ログインし直してください。");
            } else if ("success" == data.result) {
                // 成功
                $("#popupNotice #popupMsg").html("フィード【" + data.title + "】の追加が完了しました。");
                if (data.className != "") {
                    $("." + data.className).hide();
                }
                $(".feed_list_ul").listview().listview('refresh');
                $("#popupNotice").popup("open");
            } else {
                // 失敗
                alert("フィード【" + data.title + "】の追加に失敗しました。暫くしてから再度お試しください。");
                logger.error("フィード【" + data.title + "】の追加に失敗");
            }
        },
        error: function(XMLHttpRequest, statusText, errorThrown) {
            var errorMsg="Javascript Error:"+XMLHttpRequest.status+" "+XMLHttpRequest.statusText+", ";
            errorMsg=errorMsg+"error detail: "+errorThrown;
            logger.error(errorMsg);
        },
         complete: function() {
            finishLoadingEffect();
        }
    });

}

//+ フィード追加関連終了 ++++++++++++++++++++++++++++++++++++++++++++++++++++++//