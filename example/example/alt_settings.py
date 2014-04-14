#!/usr/bin/env python
# encoding: utf-8

KEY_PARAMETER_NAME = "token"
KEY_EXPIRATION_DELTA = 2
KEY_PATTERN = r"[0-9]{3,4}"
KEY_LAST_USED_UPDATE = False
KEY_AUTH_401_CONTENT = "Not authorized"
KEY_AUTH_403_CONTENT = "Forbidden"
KEY_AUTH_401_CONTENT_TYPE = 'application/javascript; charset=utf-8'
KEY_AUTH_403_CONTENT_TYPE = 'application/json; charset=utf-8'
KEY_AUTH_401_TEMPLATE = {
    "template_name": "401.html"
}
KEY_AUTH_403_TEMPLATE = {
    "template_name": "403.html"
}
KEY_TYPES = ( ('S', 'server'), ('B', 'browser'), ('M', 'mobile') )

from .settings import *
