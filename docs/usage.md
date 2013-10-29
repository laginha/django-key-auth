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

If you wish all your views to be protected, use the `KeyRequiredMiddleware`. However, through this middleware it is not possible to require a key that belongs to a `Group` or has `Permission`. 

```python
MIDDLEWARE_CLASSES = (
    ...
    'keyauth.middleware.KeyRequiredMiddleware',
)
```


## Decorator

To protect a specific view use the `key_required` decorator

```python
from keyauth.decorators import key_required

@key_required()
def view(request):
    ...
```

When requesting the resource, the app looks for the `key` parameter in the *HTTP* request to proceed with the authentication

    http://example.com/foo/1/?key=somekey

You can change the name of the parameter through the `KEY_PARAMETER_NAME` setting (more about keyauth settings [here](settings.md)).

### Require key that belongs to a Group

```python
from keyauth.decorators import key_required

@key_required(group='groupname')
def view(request):
    ...
```

### Require key that has permission

```python
from keyauth.decorators import key_required

@key_required(perm='app.someperm')
def view(request):
    ...
```

## Authorizarion

The client is authorized to access the view:

1. if there is a `Consumer` with the client's *IP* that is explicitly allowed to use the given key.
2. if there is no `Consumer` with a different *IP* explicitly allowed to use the given key.
