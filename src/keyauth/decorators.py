#!/usr/bin/env python
# encoding: utf-8
from .utils import validate_key, HttpResponse401, HttpResponse403
from .exceptions import AccessUnauthorized, AccessForbidden

def key_required(group=None, perm=None, keytype=None):
    """
    Decorator for key authentication
    """
    def decorator(f):
        def wrapper(request, *args, **kwargs):
            try:
                validate_key( request, group, perm, keytype )
                return f(request, *args, **kwargs)
            except AccessUnauthorized:
                return HttpResponse401( request )
            except AccessForbidden:
                return HttpResponse403( request )
        return wrapper 
    return decorator
