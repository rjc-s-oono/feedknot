//+ フィード追加関連 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

$(function() {
    $('#addFeedBtn').on('click', function() {
        var rssUrl = $('#rss-url').val();
        if (rssUrl == "") {
            alert("フィードURLを入力してください。");
            return false;
        }
        addFeed(rssUrl);
    });
});

// タッチしたフィードをDBに追加
function addFeed(url) {
    if (!startLoadingEffect("Adding...")) {
        return;
    }

    $("form#feed_form #url").val(url);

    // フィードを追加
    $.ajax({
        type: "POST",
        url: $("form#feed_form").attr("action"),
        data: $("form#feed_form").serialize(),
        dataType: "json",
        success: function(data, status, xhr) {
            if(data.result == 'error') {
                if (data.errors) {
                    var errorList = [];
                    for(var key in data.errors) {
                        errorList = errorList.concat(data.errors[key]);
                    }
                    alert(errorList.join("<br />"));
                }
            } else if(data.result == 'error2') {
                alert("選択したフィードはすでに設定済です。");
            } else if (data == null || undefined == data.title || undefined == data.result) {
                alert("フィードの追加に失敗しました。ログインし直してください。");
            } else if ("success" == data.result) {
                // 成功
                $('#rss-url').val('');
                $("#popupNotice #popupMsg").html("フィード【" + data.title + "】の追加が完了しました。");
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