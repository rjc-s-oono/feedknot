
// ダイアログを開く
function dialog(dialogName){
	$("<a href='" + dialogName + "' data-rel='dialog'></a>").click().remove();
}

