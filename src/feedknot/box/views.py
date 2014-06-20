# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson

from common.decorators import ajax_view

from box.models import Box
from feed.models import Feed, Article

from administration.models import LoginMaster

from box.forms import EditBoxNameForm, EditBoxPriorityForm, DeleteBoxForm

logger = logging.getLogger('application')

@login_required
def commonEdit(request):

    user = request.user
    logger.debug("user_id: %s" % (user.id))

    login_info = LoginMaster.objects.get(user=user)
    default_box_id = login_info.default_box.id

    box_list = Box.objects.filter(user=user, del_flg=False).order_by('box_priority')
    logger.debug(box_list)

    return render(request,
                  'feedknot/CommonEdit.html',
                  {'box_list' : box_list,
                   'default_box_id' : default_box_id,
                   'box_priority_array': [3, 2, 1]
                   })

# ボックス登録
@login_required
def add_box(request):

    try:
        # フィード登録
        box = Box(
            box_name="新規ボックス",
            user=request.user,
        )
        box.add_box()
    except Exception:
        # ボックスの登録失敗
        return HttpResponseRedirect(reverse('common_error'))

    return HttpResponseRedirect(reverse('common_edit'))

# ボックス名変更
@ajax_view(FormClass=EditBoxNameForm ,login_required=True)
def edit_box_name(request):

    edit_box_form = EditBoxNameForm(request.POST)
    edit_box_form.is_valid()

    box_id = edit_box_form.cleaned_data['box_id']
    box_name = edit_box_form.cleaned_data['box_name']

    try:
        box = Box.objects.get(id=box_id, user=request.user, del_flg=False)
        box.edit_box_name(box_name)

        result = {'result': 'success'}
    except Box.DoesNotExist:
        result = {'result': 'error',
                  'message': 'Box does not exist.[box_id=' + str(box_id) + ']'}
    except Exception:
        # ボックスの更新失敗
        result = {'result': 'error',
                  'message': 'update box name faild.[box_id=' + str(box_id) + ']'}

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')

# ボックス優先度変更
@ajax_view(FormClass=EditBoxPriorityForm ,login_required=True)
def edit_box_priority(request):

    edit_box_form = EditBoxPriorityForm(request.POST)
    edit_box_form.is_valid()

    box_id = edit_box_form.cleaned_data['box_id']
    box_priority = edit_box_form.cleaned_data['box_priority']

    try:
        box = Box.objects.get(id=box_id, user=request.user)
        box.edit_box_priority(box_priority);

        login_info = LoginMaster.objects.get(user=request.user)
        default_box_id = login_info.default_box.id

        box_list = Box.objects.filter(user=request.user, del_flg=False).order_by('box_priority')

        result = {'result': 'success',
                  'default_box_id' : default_box_id,
                  'box_list': [box.as_json() for box in box_list],
                  'box_priority_array': [3, 2, 1]}
    except Box.DoesNotExist:
        result = {'result': 'error',
                  'message': 'Box does not exist.[box_id=' + str(box_id) + ']'}
    except Exception:
        # ボックスの更新失敗
        result = {'result': 'error',
                  'message': 'update box priority faild.[box_id=' + str(box_id) + ']'}

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')

# ボックス削除
@ajax_view(FormClass=DeleteBoxForm ,login_required=True)
def del_box(request):

    delete_box_form = DeleteBoxForm(request.POST)
    delete_box_form.is_valid()

    box_id = delete_box_form.cleaned_data['box_id']

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        login_info = LoginMaster.objects.get(user=request.user)
        default_box_id = login_info.default_box.id

        if default_box_id != box_id:
            box = Box.objects.get(pk=box_id, user=request.user)
            feed_list = box.feed_box.all()
            article_list = box.article_box.all()
            article_list.delete()
            feed_list.delete()
            box.delete()

            box_list = Box.objects.filter(user=request.user, del_flg=False).order_by('box_priority')

            result = {'result': 'success',
                      'default_box_id' : default_box_id,
                      'box_list': [box.as_json() for box in box_list],
                      'box_priority_array': [3, 2, 1]}
        else:
            result = {'result': 'warn',
                      'message': 'Box is default box.[box_id=' + str(box_id) + ']'}
    except Box.DoesNotExist:
        result = {'result': 'error',
                  'message': 'Box does not exist.[box_id=' + str(box_id) + ']'}
    except Exception:
        # ボックスの削除失敗
        result = {'result': 'error',
                  'message': 'delete box faild.[box_id=' + str(box_id) + ']'}

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')
