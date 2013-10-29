# Middlewares

## KeyRequiredMiddleware

Add this middleware to protect all views with key authetication.

```python
MIDDLEWARE_CLASSES = (
    ...
    'keyauth.middleware.KeyRequiredMiddleware',
)
```

## KeyAuthenticationMiddleware

Middleware to authenticate user through given key. (Required)

```python
MIDDLEWARE_CLASSES = (
    ...
    'keyauth.middleware.KeyAuthenticationMiddleware',
)
```
