# encoding: UTF-8
import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

from common.decorators import ajax_view

logger = logging.getLogger('application')
js_logger = logging.getLogger('js')

def err(request):
    return render(request, 'error.html')

def err_500(request):
    return render(request, '500.html')

@csrf_exempt
@ajax_view()
def write_logging(request):

    loglevel = request.REQUEST.get('loglevel', '')
    message = request.REQUEST.get('message', '')

    log_pattern = {
        "FATAL": (lambda x: js_logger.critical(x)),
        "ERROR": (lambda x: js_logger.error(x)),
        "WARN": (lambda x: js_logger.warning(x)),
        "INFO": (lambda x: js_logger.info(x)),
        "DEBUG": (lambda x: js_logger.debug(x)),
        "TRACE": (lambda x: js_logger.debug(x)),
    }

    if loglevel in log_pattern.keys():
        log_pattern[loglevel](message)
        response_dict = {'status':'sucsess'}

    else:
        logger.warning('Loglevel is not found in a request.')
        response_dict = {'status':'failure', 'result':'Request parameter injustice'}

    values = simplejson.dumps(response_dict, ensure_ascii=False)
    return HttpResponse(values, mimetype="text/javascript")
