# django-key-auth

Key based authentication for Django

```python
@key_required()
def view(request):
    key = request.key
    ...
```

[Read the docs!](docs/index.md)


## Install

    pip install git+https://github.com/laginha/django-key-auth/


## Features

- Authentication per view.
- Authentication middleware.
- Authentication backend.
- Django's Permissions and Groups integrated.
- Per key black and white-lists based on client's _IP_ address.


## ToDo

- Add Redis support
