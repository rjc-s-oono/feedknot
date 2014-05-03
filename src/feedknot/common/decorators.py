# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils import simplejson
from functools import wraps

logger = logging.getLogger('application')

_400_ERROR = '400 Bad Request'
_403_ERROR = '403 Forbidden'
_405_ERROR = '405 Not Allowed'

_ERROR_MSG = '<!DOCTYPE html><html lang="ja"><body><h1>%s</h1><p>%%s</p></body></html>'
_400_ERROR_MSG = _ERROR_MSG % _400_ERROR
_403_ERROR_MSG = _ERROR_MSG % _403_ERROR
_405_ERROR_MSG = _ERROR_MSG % _405_ERROR

def ajax_view(FormClass=None, method='POST', login_required=False, ajax_required=True, json_form_errors=False):
    def decorator(view_func):
        def _ajax_view(request, *args, **kwargs):
            request_url = request.build_absolute_uri()
            if request.method != method and method != 'REQUEST':
                logger.error(_405_ERROR + (': Request url [%s]' % request_url))
                logger.error(_405_ERROR + (': Request must be a %s.' % method))
                return HttpResponseNotAllowed(mark_safe(_405_ERROR_MSG % ('Request must be a %s.' % method)))

            if ajax_required and not request.is_ajax():
                logger.error(_403_ERROR + (': Request url [%s]' % request_url))
                logger.error(_403_ERROR + ': Request must be set via AJAX.')
                return HttpResponseForbidden(mark_safe(_403_ERROR_MSG % 'Request must be set via AJAX.'))

            if login_required and not request.user.is_authenticated():
                logger.error(_403_ERROR + (': Request url [%s]' % request_url))
                logger.error(_403_ERROR + ': User must be authenticated!')
                return HttpResponseForbidden(mark_safe(_403_ERROR_MSG % 'User must be authenticated!'))

            if FormClass:
                f = FormClass(getattr(request, method))
                if not f.is_valid():
                    errors = dict((k, [unicode(x) for x in v]) for k,v in f.errors.items())
                    logger.error(_400_ERROR + (': Request url [%s]' % request_url))
                    logger.error(_400_ERROR + ': Invalid form ' + errors)

                    if json_form_errors:
                        return HttpResponse(simplejson.dumps({'error': 'form', 'errors': errors}), 'application/json')
                    else:
                        return HttpResponseBadRequest(mark_safe(_400_ERROR_MSG % ('Invalid form<br />' + f.errors.as_ul())))
                request.form = f

            return view_func(request, *args, **kwargs)
        return wraps(view_func)(_ajax_view)
    return decorator
