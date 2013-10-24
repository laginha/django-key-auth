#!/usr/bin/env python
# encoding: utf-8
from .models import Consumer
from .consts import KEY_LAST_USED_UPDATE


def is_valid_key(request):
    '''
    Validate the given key
    '''
    if request.user.is_authenticated():
        if request.key and is_valid_consumer(request):
            if KEY_LAST_USED_UPDATE:
                request.key.save()
            return True
    return False


def is_valid_consumer(request):
    '''
    Validate the client for view/resource access with the given key
    '''
    try:
        ip = request.META.get('REMOTE_ADDR', None)
        return Consumer.objects.get(key=request.key, ip=ip).allowed
    except Consumer.DoesNotExist:
        consumers = Consumer.objects.filter(key=request.key, allowed=True)
        return not consumers.exists()
