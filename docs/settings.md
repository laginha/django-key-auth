# Settings

All this settings must go before `INSTALLED_APPS`


### KEY\_PARAMETER_NAME 

The name of the parameter used for the key token. Defaults to `key`.

```python
KEY_PARAMETER_NAME = "foo"
```

### KEY\_AUTH\_401_CONTENT

Message to return in case key based authentication fails token validation.

```python
KEY_AUTH_401_CONTENT = "You are not authorized to access this resource"
```

### KEY\_AUTH\_403_CONTENT

Message to return in case key based authentication fails due to lack of permissions.

```python
KEY_AUTH_403_CONTENT = "You are forbidded to access this resource"
```

### KEY\_AUTH\_401_TEMPLATE

Template to render in case key based authentication fails token validation. This setting has priority over `KEY_AUTH_401_CONTENT`. 

```python
KEY_AUTH_401_TEMPLATE = {
    "template_name": "401.html"
}
```

### KEY\_AUTH\_403_TEMPLATE

Template to render in case key based authentication fails due to lack of permissions. This setting has priority over `KEY_AUTH_403_CONTENT`. 

```python
KEY_AUTH_403_TEMPLATE = {
    "template_name": "403.html"
}
```
 
The keys to `KEY_AUTH_401_TEMPLATE` are the arguments expected for `django.shortcuts.render`.

### KEY_AUTH\_401\_CONTENT\_TYPE

Content type for the Not Authorized response. Default to `text/html; charset=utf-8`.

```python
KEY_AUTH_401_CONTENT_TYPE = 'application/javascript; charset=utf-8' #JSONP
```

### KEY_AUTH\_403\_CONTENT\_TYPE

Content type for the Forbidden response. Default to `text/html; charset=utf-8`.

```python
KEY_AUTH_403_CONTENT_TYPE = 'application/json; charset=utf-8' #JSON
```

### KEY\_EXPIRATION_DELTA

The number of years between the activation date and the expiration date of a key token. Defaults to `1`.

```python
KEY_EXPIRATION_DELTA = 2
```

### KEY_PATTERN   

The regex pattern of the generated key token. Defaults to `r"[a-z0-9A-Z]{30,40}"`

```python
KEY_PATTERN = r"[a-zA-Z0-9]{10}"
```

### KEY_LAST\_USED\_UPDATE

Update `last_used` model attribute for the given key. Defaults to `True`.

```python
KEY_LAST_USED_UPDATE = False
```

### KEY_TYPE\_CHOICES

The choices for the type of key. Default to `(('S', 'server'), ('B', 'browser'))`.

```python
KEY_TYPE_CHOICES = (('M', 'Mobile'), ('S', 'server'), ('B', 'browser'))
````

## KEY_TYPE\_VALIDATIONS

Dictionary of validations for each type in `KEY_TYPE_CHOICES`. These are used to obtain the key suitability for a given request.

```python
from django_mobileesp.utils import is_browser_agent, is_mobile_agent
from django_mobileesp.utils import is_tablet_agent, is_smartphone_agent

KEY_TYPE_VALIDATIONS  = {
    'browser':    lambda request: is_browser_agent( request ),
    'server':     lambda request: not is_browser_agent( request ),
    'mobile':     lambda request: is_mobile_agent( request ),
    'tablet':     lambda request: is_tablet_agent( request ),
    'smartphone': lambda request: is_smartphone_agent( request ),
}
```
