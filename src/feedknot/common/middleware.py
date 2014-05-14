# -*- coding: utf-8 -*-
import logging

from django.conf import settings

logger = logging.getLogger('common_log')

class loggingMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request):
        """
        実行view決定前にコール
        """
        method = request.method
        request_url = request.get_full_path()
        request_abs_url = request.build_absolute_uri()
        request_param = request.REQUEST
        cookies = request.COOKIES
        meta = request.META

        if not request_url.startswith(settings.MEDIA_URL) and  not request_url.startswith(settings.STATIC_URL):
            logger.info('%s %s' % (method, request_abs_url))
            logger.debug('======================== Request Info Start ==================================')
            logger.debug('Request Param: %s' % request_param)
            logger.debug('Cookies: %s' % cookies)
            logger.debug('Meta: %s' % meta)
            logger.debug('======================== Request Info End ====================================')

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        実行view決定後にコール
        """
        request_url = request.get_full_path()

        if not request_url.startswith(settings.MEDIA_URL) and  not request_url.startswith(settings.STATIC_URL):
            logger.info('Call Module: %s, Call Function: %s' % (view_func.__module__, view_func.__name__))
            logger.info('view_args: %s, view_kwargs: %s' % (view_args, view_kwargs))

        return None

    def process_response(self, request, response):
        """
        view実行後にコール
        """
        method = request.method
        request_url = request.get_full_path()
        request_abs_url = request.build_absolute_uri()

        status_code = response.status_code

        logger.info('%s %s [%s]' % (method, request_abs_url, status_code))

        if not request_url.startswith(settings.MEDIA_URL) and  not request_url.startswith(settings.STATIC_URL):
            logger.debug('Content-Type: [%s]' % (response['Content-Type']))

        return response
