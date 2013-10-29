#!/usr/bin/env python
# encoding: utf-8
from .utils import is_valid_key, HttpResponse401

def key_required(group=None, perm=None):
    """
    Decorator for key authentication
    """
    def decorator(f):
        def wrapper(request, *args, **kwargs):
            if is_valid_key( request, group, perm ):
                return f(request, *args, **kwargs)
            return HttpResponse401( request )
        return wrapper 
    return decorator
