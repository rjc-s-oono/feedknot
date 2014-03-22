# encoding: UTF-8
import logging
from django.conf import settings

logger = logging.getLogger('application')

def staticQueryString(request):
    return {'QUERY_STRING': settings.QUERY_STRING}

