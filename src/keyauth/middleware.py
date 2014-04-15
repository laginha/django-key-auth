#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from .utils import validate_key, get_key, HttpResponse401, HttpResponse403
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
        request.key  = SimpleLazyObject(lambda: get_key(request))
        request.user = SimpleLazyObject(lambda: request.key.user if request.key else AnonymousUser())


class SuitableKeyMiddleware(object):
    """
    Middleware to Checks if request.key is suitable for the request 
    according to key type and request's user agent.
    """
    def process_request(self, request): 
        if request.key and not request.key.is_suitable( request ):
            return HttpResponse403( request )
        