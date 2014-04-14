#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from .models import Consumer
from .consts import KEY_LAST_USED_UPDATE, KEY_AUTH_401_TEMPLATE, KEY_AUTH_401_CONTENT_TYPE, KEY_AUTH_401_CONTENT
from .consts import KEY_AUTH_403_TEMPLATE, KEY_AUTH_403_CONTENT_TYPE, KEY_AUTH_403_CONTENT, KEY_PARAMETER_NAME
from .exceptions import AccessForbidden, AccessUnauthorized


def validate_key(request, group=None, perm=None, keytype=None):
    """
    Validate the given key
    """
    def update_last_access():
        if KEY_LAST_USED_UPDATE:
            request.key.save()
    
    if request.user.is_authenticated() and is_valid_consumer(request):
        if not group and not perm and not keytype:
            return update_last_access()
        elif keytype:
            if request.key.is_type( keytype ):
                return update_last_access()
        elif group:
            if request.key.belongs_to_group( group ):
                return update_last_access()
        elif perm:
            if request.key.has_perm( perm ):
                return update_last_access()
        raise AccessForbidden
    raise AccessUnauthorized


def is_valid_consumer(request):
    """
    Validate the client for view/resource access with the given key
    
    The client is authorized to access the view:
        - if there is a `Consumer` with the client's *IP* that is explicitly allowed to use the given key,
        - if there is no `Consumer` with a different *IP* explicitly allowed to use the given key
    """
    try:
        ip = request.META.get('REMOTE_ADDR', None)
        return Consumer.objects.get(key=request.key, ip=ip).allowed
    except Consumer.DoesNotExist:
        consumers = Consumer.objects.filter(key=request.key, allowed=True)
        return not consumers.exists()


def get_key(request):
    return authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
    

def AccessFailedResponse(request, template, content, content_type, status):
    if template:
        content_type = template.pop('content_type', content_type)
        return render(request, status=status, content_type=content_type, **template)
    return HttpResponse(content, status=status, content_type=content_type)


def HttpResponse401(request, template=KEY_AUTH_401_TEMPLATE,
content=KEY_AUTH_401_CONTENT, content_type=KEY_AUTH_401_CONTENT_TYPE):
    """
    HTTP response for not-authorized access (status code 403)
    """
    return AccessFailedResponse(request, template, content, content_type, status=401)

   
def HttpResponse403(request, template=KEY_AUTH_403_TEMPLATE,
content=KEY_AUTH_403_CONTENT, content_type=KEY_AUTH_403_CONTENT_TYPE):
    """
    HTTP response for forbidden access (status code 403)
    """
    return AccessFailedResponse(request, template, content, content_type, status=403)
    
