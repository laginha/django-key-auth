# django-key-auth

Key based authentication for Django

```python
@key_required()
def view(request):
    ...
```

[See the docs!](docs/usage.md)


## Install

    pip install git+https://github.com/laginha/django-key-auth/


## Features

- Authentication per view.
- Authentication middleware.
- Authentication backend.
- Django's Permissions and Groups integrated.
- Key usage white list based on client's _IP_ address.


## ToDo

- Add Redis support
