
// フィード検索機能 ロード
google.load("feeds", "1");

// ダイアログを開く
function dialog(dialogName){
    $("<a href='" + dialogName + "' data-rel='dialog'></a>").click().remove();
}

//+ くるくる関連 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

// くるくる中 判定フラグ
var isWaiting = false;

// くるくる開始
function startLoadingEffect(msg) {
    if (isWaiting) {
        alert("通信中です。しばらくお待ちください。");
        return false;
    }
    isWaiting = true;
    $.mobile.loading( 'show', {
        text: msg,
        textVisible: true,
        theme: 'z',
        html: ""
    });
    return true;
}

// くるくる終了
function finishLoadingEffect() {
    isWaiting = false;
    $.mobile.loading( 'hide', {});
}

//+ くるくる関連終了 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

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

                var tag = "<li data-theme=\"c\" id=\"feedLI\" data-icon=\"plus\" class=\"feedLI" + i + "\">" +
                          "<a onclick=\"addFeed('#link#', '#title#','feedLI" + i + "')\">#title#</a>" +
                          "</li>";
                tag = tag.replace("#link#", link);
                tag = tag.replace("#title#", title);
                tag = tag.replace("#title#", title);

                $(".feed_list_ul")
                    .attr("data-role","listview")
                    .append(tag);

                //alert(link);
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
            if (data == null) {
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

//+ ボックス追加関連 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

// ボックスを追加
function addBox(formName) {
    if ( ! startLoadingEffect("Adding...")) {
        return;
    }
    $.ajax({
        type: "POST",
        url: $(formName).attr("action"),
        data: $(formName).serialize(),    // フォームをシリアライズ化して送信
        dataType: "json",
        success: function(data, status, xhr) {
            if (data == null) {
                alert("ボックスの追加に失敗しました。ログインし直してください。");
            } else if ("success" == data.result) {
                // 成功
                $("#popupNotice #popupMsg").html("ボックス【" + data.boxName + "】の追加が完了しました。");

                // TODO ★ ここにボックス追加後の処理を書く

                $("#popupNotice").popup("open");
            } else {
                // 失敗
                alert("ボックス【" + data.boxName + "】の追加に失敗しました。暫くしてから再度お試しください。");
            }
            finishLoadingEffect();
        },
        error: function() {
            finishLoadingEffect();
            alert("失敗！");
        }
    });

}

//+ ボックス追加関連終了 ++++++++++++++++++++++++++++++++++++++++++++++++++++++//
