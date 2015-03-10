#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django_mobileesp.utils import is_browser_agent, is_mobile_agent, is_tablet_agent, is_smartphone_agent

'''
DEFAULT VALUES
'''
DEFAULT_KEY_LAST_USED_UPDATE  = True
DEFAULT_KEY_EXPIRATION_DELTA  = 365
DEFAULT_KEY_PATTERN           = r"[a-z0-9A-Z]{30,40}"
DEFAULT_KEY_PARAMATER_NAME    = 'key'
DEFAULT_KEY_AUTH_401_TEMPLATE = DEFAULT_KEY_AUTH_403_TEMPLATE = None
DEFAULT_KEY_AUTH_401_CONTENT  = DEFAULT_KEY_AUTH_403_CONTENT = ""
DEFAULT_CONTENT_TYPE          = 'text/html; charset=utf-8'
DEFAULT_KEY_TYPE_CHOICES      = ( ('S', 'server'), ('B', 'browser') )
DEFAULT_KEY_TYPE_VALIDATIONS  = {
    'browser':    lambda request: is_browser_agent( request ),
    'server':     lambda request: not is_browser_agent( request ),
    'mobile':     lambda request: is_mobile_agent( request ),
    'tablet':     lambda request: is_tablet_agent( request ),
    'smartphone': lambda request: is_smartphone_agent( request ),
}

'''
SETTINGS
'''
KEY_LAST_USED_UPDATE      = getattr(settings, 'KEY_LAST_USED_UPDATE', DEFAULT_KEY_LAST_USED_UPDATE)
KEY_EXPIRATION_DELTA      = getattr(settings, "KEY_EXPIRATION_DELTA", DEFAULT_KEY_EXPIRATION_DELTA)
KEY_PATTERN               = getattr(settings, "KEY_PATTERN", DEFAULT_KEY_PATTERN)
KEY_PARAMETER_NAME        = getattr(settings, 'KEY_PARAMETER_NAME', DEFAULT_KEY_PARAMATER_NAME)
KEY_AUTH_401_TEMPLATE     = getattr(settings, 'KEY_AUTH_401_TEMPLATE', DEFAULT_KEY_AUTH_401_TEMPLATE)
KEY_AUTH_401_CONTENT      = getattr(settings, 'KEY_AUTH_401_CONTENT', DEFAULT_KEY_AUTH_401_CONTENT)
KEY_AUTH_401_CONTENT_TYPE = getattr(settings, 'KEY_AUTH_401_CONTENT_TYPE', DEFAULT_CONTENT_TYPE)
KEY_AUTH_403_TEMPLATE     = getattr(settings, 'KEY_AUTH_401_TEMPLATE', DEFAULT_KEY_AUTH_403_TEMPLATE)
KEY_AUTH_403_CONTENT      = getattr(settings, 'KEY_AUTH_401_CONTENT', DEFAULT_KEY_AUTH_403_CONTENT)
KEY_AUTH_403_CONTENT_TYPE = getattr(settings, 'KEY_AUTH_401_CONTENT_TYPE', DEFAULT_CONTENT_TYPE)
KEY_TYPE_CHOICES          = getattr(settings, 'KEY_TYPE_CHOICES', DEFAULT_KEY_TYPE_CHOICES)
KEY_TYPE_VALIDATIONS      = getattr(settings, "KEY_TYPE_VALIDATIONS", DEFAULT_KEY_TYPE_VALIDATIONS)
