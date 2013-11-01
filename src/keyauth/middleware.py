#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth import authenticate
from .utils import validate_key, HttpResponse401, HttpResponse403
from .consts import KEY_PARAMETER_NAME
from .exceptions import AccessUnauthorized, AccessForbidden


class KeyRequiredMiddleware(object):
    """
    Middleware to check for Key in request and validate the Consumer
    """
    def process_request(self, request):
        try:
            validate_key(request)
        except AccessUnauthorized:
            return HttpResponse401( request )
        except AccessForbidden:
            return HttpResponse403( request )


class KeyAuthenticationMiddleware(object):
    """
    Middleware to authenticate user through given key
    """
    def process_request(self, request):        
        key = authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
        request.key = key
        if key:
            request.user = key.user
