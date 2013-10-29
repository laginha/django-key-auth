# Settings

All this settings must go before `INSTALLED_APPS`


### KEY\_PARAMETER_NAME 

The name of the parameter used for the key token. Defaults to `key`.

```python
KEY_PARAMETER_NAME = "foo"
```

### KEY\_AUTH\_401_CONTENT

Message to return in case key based authentication fails.

```python
KEY_AUTH_401_CONTENT = "You are not authorized"
```

### KEY\_AUTH\_401_TEMPLATE

Template to render in case key based authentication fails. This setting has priority over `KEY_AUTH_401_CONTENT`. 

```python
KEY_AUTH_401_TEMPLATE = {
    "template_name": "401.html"
}
```
 
The keys to `KEY_AUTH_401_TEMPLATE` are the arguments expected for `django.shortcuts.render`.

### KEY_AUTH\_401\_CONTENT\_TYPE

Content type for the Not Authorized response

```python
KEY_AUTH_401_CONTENT_TYPE = 'application/json; charset=utf-8' #JSON
KEY_AUTH_401_CONTENT_TYPE = 'application/javascript; charset=utf-8' #JSONP
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
