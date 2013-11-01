#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.models import User, Permission, Group
from .models import Key


class KeyAuthBackend(object):
    """
    Authentication backend
    """
    def authenticate(self, token=None):
        keys = Key.objects.filter(token=token).select_related('user')
        if keys and not keys[0].has_expired():
            return keys[0]
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
