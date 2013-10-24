#!/usr/bin/env python
# encoding: utf-8
from .settings import *
from keyauth.consts import JSONP_CONTENT_TYPE

KEY_AUTH_401_CONTENT = "Not authorized"
KEY_AUTH_401_CONTENT_TYPE = JSONP_CONTENT_TYPE
KEY_EXPIRATION_DELTA = 2
KEY_PATTERN = r"[0-9]{3,4}"
KEY_AUTH_401_TEMPLATE = {
    "template_name": "401.html"
}
KEY_LAST_USED_UPDATE = False
