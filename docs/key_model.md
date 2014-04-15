# Key Model


## Attributes

### groups

Many to many relation to django's `Group`.

### permissions

Many to many relation to django's `Permisson`.

### user

Foreign key to django's `User`.

### consumers

Related field for `Consumers` with this `Key`.

### token

The key's string token. 

### activation_date

The date of creation of `Key`.

### expiration_date 

The date from which the key will no longer be valid (by default, one year after creation).

### last_used

The datetime of the last access using the key, if `KEY_LAST_USED_UPDATE` set to `True` (default behavior).

### key_type

The type of the key. By default is `None`, which means the key is a generic type. The allowed choices are specified by the `KEY_TYPE_CHOICES` setting.


## Methods

### belongs_to\_group

Checks if `key` belongs to a django's auth `Group`.

```python
key.belongs_to_group('name')
```

### has_perm

Checks if `key` has the given django's auth `Permission`.

```python
key.has_perm('app_label.perm')
```

### add_consumer

Add consumer based on its _ip_ address.  If `key` has consumers it means, only those consumers can use the `key`.

```python
key.add_consumer('127.0.0.1')
```

### clear_consumers

Remove all consumers. This means there is no longer usage restrictions and everyone can use the `key`.

```python
key.clear_consumers()
```

### get_consumers

Get all consumers for this `key`.

```python
key.get_consumers() #the same as key.consumers.all()
```

### extend_expiration\_date

Extend expiration date a number of given years (defaults to 1).

```python
key.extend_expiration_date(years=1)
```

### refresh_token

Replace `token` with a new generated one, according to a given pattern that defaults to `KEY_PATTERN` setting.

```python
key.refresh_token(pattern='[0-9]{3,4}')
```

### is_type

Checks if key is of a given type.

```python
key.is_type('browser')
```

### get_type

Get the type name of key

```python
key.get_type()
```

### is_suitable

Checks if key is suitable for given request according to key type and request's user agent.

```python
key.is_suitable( request )
```


## QuerySet Manager

### expired

Filter keys that have expired (no longer valid).

```python
Key.objects.expired()
```

### not_expired

Filter keys that have yet to expired (still valid).

```python
Key.objects.not_expired()
