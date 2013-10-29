#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import Consumer
from .consts import KEY_LAST_USED_UPDATE, KEY_AUTH_401_TEMPLATE
from .consts import KEY_AUTH_401_CONTENT_TYPE, KEY_AUTH_401_CONTENT


def is_valid_key(request, group=None, perm=None):
    """
    Validate the given key
    """
    no_restrictions = lambda: not group and not perm
    key_in_group = lambda: group and request.key.belongs_to_group( group )
    key_has_perm = lambda: perm and request.key.has_perm( perm )

    if request.user.is_authenticated() and is_valid_consumer(request):
        if no_restrictions() or key_in_group() or key_has_perm():
            if KEY_LAST_USED_UPDATE:
                request.key.save()
            return True      
    return False


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


def HttpResponse401(request, template=KEY_AUTH_401_TEMPLATE,
content=KEY_AUTH_401_CONTENT, content_type=KEY_AUTH_401_CONTENT_TYPE):
    """
    Not authorized HTTP response
    """
    if template:
        content_type = template.pop('content_type', content_type)
        return render(request, status=401, content_type=content_type, **template)
    return HttpResponse(content, status=401, content_type=content_type)

