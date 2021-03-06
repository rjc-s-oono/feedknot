
function editDefaultBox(box_id) {
    if (!startLoadingEffect("Adding...")) {
        return;
    }

    var $boxEditDefaultFrom = $('#box-edit-default-from');
    $('#default_box_id').val(box_id);

    $.ajax({

        type: 'POST',
        url: $boxEditDefaultFrom.attr('action'),
        data: $boxEditDefaultFrom.serialize(),
        dataType: "json",
        success: function(data, status) {
            if (data.result == "success") {
                logger.debug(data);
            } else {
                logger.error(data.message);
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

function editBoxName(box_id, box_name) {
    if (!startLoadingEffect("Adding...")) {
        return;
    }

    var $boxEditNameFrom = $('#box-edit-name-from');
    $('#edit_name_box_id').val(box_id);
    $('#box_name').val(box_name);

    $.ajax({
        type: 'POST',
        url: $boxEditNameFrom.attr('action'),
        data: $boxEditNameFrom.serialize(),
        dataType: "json",
        success: function(data, status) {
            if (data.result == "success") {
                logger.debug(data);
            } else {
                logger.error(data.message);
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

function editBoxPriority(box_id, box_priority) {
    if (!startLoadingEffect("Adding...")) {
        return;
    }

    var $boxEditNameFrom = $('#box-edit-priority-from');
    $('#edit_priority_box_id').val(box_id);
    $('#box_priority').val(box_priority);

    $.ajax({
        type: 'POST',
        url: $boxEditNameFrom.attr('action'),
        data: $boxEditNameFrom.serialize(),
        dataType: "json",
        success: function(data, status) {
            if (data.result == "success") {
                var template  = _.template($('#box-list-template').text());
                $("#box-list").html(template(data)).trigger('create');
            } else {
                logger.error(data.message);
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

function deleteBox(box_id) {
    if (!startLoadingEffect("Adding...")) {
        return;
    }

    var $boxDeleteForm = $('#box-delete-form');
    $('#delete_box_id').val(box_id);

    $.ajax({
        type: 'POST',
        url: $boxDeleteForm.attr('action'),
        data: $boxDeleteForm.serialize(),
        dataType: "json",
        success: function(data, status) {
            if (data.result == "success") {
                var template  = _.template($('#box-list-template').text());
                $("#box-list").html(template(data)).trigger('create');
            } else if (data.result == "warn") {
                $("#popupNotice #popupMsg").html("デフォルト設定されているため削除できません");
                $("#popupNotice").popup("open");
                logger.warn(data.message);
            } else {
                logger.error(data.message);
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
