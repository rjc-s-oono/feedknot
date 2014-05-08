
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
