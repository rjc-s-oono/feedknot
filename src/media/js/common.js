
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
