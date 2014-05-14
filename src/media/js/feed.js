//+ フィード追加関連 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

// フィード検索開始 (Google findFeeds)
function searchFeed(searchTxt) {
    //alert("検索値：" + searchTxt);
    if ( ! startLoadingEffect("Searching...")) {
        return;
    }
    google.feeds.findFeeds(searchTxt, dispFeed);
}

// 検索結果 (Google findFeeds)
function dispFeed(result) {
    //alert("dispFeed: start");
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
                          "<a onclick=\"addFeed('#url#', '#title#','feedLI" + i + "')\">#title#</a>" +
                          "</li>";
                //tag = tag.replace("#link#", link);
                tag = tag.replace("#url#", url);
                tag = tag.replace("#title#", title);
                tag = tag.replace("#title#", title);

                $(".feed_list_ul")
                    .attr("data-role","listview")
                    .append(tag);

                //alert(link);
                //alert(url);
            }
            $(".feed_list_ul")
                .listview().listview('refresh');
        }
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
            if (data == null || undefined == data.title || undefined == data.result) {
                alert("フィードの追加に失敗しました。ログインし直してください。");
            } else if ("success" == data.result) {
                // 成功
                //alert("フィード【" + data.title + "】の追加が完了しました。");
                $("#popupNotice #popupMsg").html("フィード【" + data.title + "】の追加が完了しました。");
                $("." + data.className).hide();
                $(".feed_list_ul").listview().listview('refresh');
                $("#popupNotice").popup("open");
            } else {
                // 失敗
                alert("フィード【" + data.title + "】の追加に失敗しました。暫くしてから再度お試しください。");
            }
            finishLoadingEffect();
        },
        error: function() {
            finishLoadingEffect();
            alert("失敗！");
        }
    });

}

//+ フィード追加関連終了 ++++++++++++++++++++++++++++++++++++++++++++++++++++++//