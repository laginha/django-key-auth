#!/usr/bin/env python
# encoding: utf-8
from .consts import HttpResponse401
from .utils import is_valid_key

def key_required(group=None, perm=None):

    def decorator(f):
        def wrapper(request, *args, **kwargs):
            if is_valid_key( request, group, perm ):
                return f(request, *args, **kwargs)
            return HttpResponse401( request )
        return wrapper
        
    return decorator
