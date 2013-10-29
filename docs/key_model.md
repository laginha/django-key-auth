# Key Model

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

### extend_expiration\_date

Extend expiration date a number of given years (defaults to 1).

```python
key.extend_expiration_date(years=1)
```


## Attributes

### groups

Many to many relation to django's `Group`.

### permissions

Many to many relation to django's `Permisson`.

### user

Foreign key to django's `User`.

### token

The key token. 

### activation_date

The date of creation of the key.

### expiration_date 

The date from which the key will expire, thus no longer valid (by default, one year after creation).

### last_used

The last time the key was used to access a resource, if `KEY_LAST_USED_UPDATE` set to `True` (default behavior).
