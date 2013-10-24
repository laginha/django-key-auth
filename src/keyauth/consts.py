#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

JSON_CONTENT_TYPE  = 'application/json; charset=utf-8'
JSONP_CONTENT_TYPE = 'application/javascript; charset=utf-8'
TEXT_CONTENT_TYPE  = 'text/html; charset=utf-8'

DEFAULT_KEY_LAST_USED_UPDATE  = True
DEFAULT_KEY_EXPIRATION_DELTA  = 1
DEFAULT_KEY_PATTERN           = r"[a-z0-9A-Z]{30,40}"
DEFAULT_KEY_PARAMATER_NAME    = 'key'
DEFAULT_KEY_AUTH_401_TEMPLATE = None
DEFAULT_KEY_AUTH_401_CONTENT  = ""

KEY_LAST_USED_UPDATE      = getattr(settings, 'KEY_LAST_USED_UPDATE', DEFAULT_KEY_LAST_USED_UPDATE)
KEY_EXPIRATION_DELTA      = getattr(settings, "KEY_EXPIRATION_DELTA", DEFAULT_KEY_EXPIRATION_DELTA)
KEY_PATTERN               = getattr(settings, "KEY_PATTERN", DEFAULT_KEY_PATTERN)
KEY_PARAMETER_NAME        = getattr(settings, 'KEY_PARAMETER_NAME', DEFAULT_KEY_PARAMATER_NAME)
KEY_AUTH_401_TEMPLATE     = getattr(settings, 'KEY_AUTH_401_TEMPLATE', DEFAULT_KEY_AUTH_401_TEMPLATE)
KEY_AUTH_401_CONTENT      = getattr(settings, 'KEY_AUTH_401_CONTENT', DEFAULT_KEY_AUTH_401_CONTENT)
KEY_AUTH_401_CONTENT_TYPE = getattr(settings, 'KEY_AUTH_401_CONTENT_TYPE', TEXT_CONTENT_TYPE)


def HttpResponse401(request, template=KEY_AUTH_401_TEMPLATE,
content=KEY_AUTH_401_CONTENT, content_type=KEY_AUTH_401_CONTENT_TYPE):
    if template:
        content_type = template.pop('content_type', content_type)
        return render(request, status=401, content_type=content_type, **template)
    return HttpResponse(content, status=401, content_type=content_type)
