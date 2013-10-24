#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.models import User
from .models import Key


class KeyAuthBackend(object):
    """
    Authentication backend
    """
    def authenticate(self, token=None):
        keys = Key.objects.filter(token=token).select_related('user')
        return keys[0] if keys.exists() else None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
