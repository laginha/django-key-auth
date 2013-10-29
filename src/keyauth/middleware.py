#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth import authenticate
from .utils import is_valid_key, HttpResponse401
from .consts import KEY_PARAMETER_NAME


class KeyRequiredMiddleware(object):
    """
    Middleware to check for Key in request and validate the Consumer
    """
    def process_request(self, request):
        if not is_valid_key(request):
            return HttpResponse401( request )


class KeyAuthenticationMiddleware(object):
    """
    Middleware to authenticate user through given key
    """
    def process_request(self, request):
        key = authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
        request.key = key
        if key: request.user = key.user
