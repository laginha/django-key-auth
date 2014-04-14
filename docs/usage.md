# Usage

## Settings

Add the following to your settings file:

```python
INSTALLED_APPS = (
    ...
    'keyauth',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'keyauth.backends.KeyAuthBackend',
)

MIDDLEWARE_CLASSES = (
    ...
    'keyauth.middleware.KeyAuthenticationMiddleware',
)
```

[More settings!](settings.md)


## Require key

```python
from keyauth.decorators import key_required

@key_required()
def view(request):
    key = request.key
    ...
```

When requesting the resource, the app looks for the `key` parameter in the _HTTP_ request to proceed with the authentication

    http://example.com/foo/1/?key=somekey

You can change the name of the parameter through the `KEY_PARAMETER_NAME` setting.

### Require key that belongs to a Group

```python
from keyauth.decorators import key_required

@key_required(group='groupname')
def view(request):
    ...
```

For more about groups, [read the Django docs](https://docs.djangoproject.com/en/dev/topics/auth/default/#permissions-and-authorization)

### Require key that has permission

```python
from keyauth.decorators import key_required

@key_required(perm='app.someperm')
def view(request):
    ...
```

For more abour permissions, [read the Django docs](https://docs.djangoproject.com/en/1.3/topics/auth/#permissions)

### Require key of a certain type

```python
from keyauth.decorators import key_required

@key_required(keytype='browser')
def view(request):
    ...
```

## Authorizarion

The client is authorized to access the view:

1. if there is a `Consumer` with the client's *IP* that is explicitly allowed to use the given key.
2. if there is no `Consumer` with a different *IP* explicitly allowed to use the given key.
3. if given key has necessary permission or belongs to a group (if required) 
