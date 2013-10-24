#!/usr/bin/env python
# encoding: utf-8
from .consts import HttpResponse401
from .utils import is_valid_key

def key_required(f):
    """
    Check for the key in request and validate the Consumer
    """
    def wrapper(request, *args, **kwargs):
        if is_valid_key( request ):
            return f(request, *args, **kwargs)
        return HttpResponse401( request )
    return wrapper
