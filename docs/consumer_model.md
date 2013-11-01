# Consumer Model


## Attributes

### key

Foreign key to `Key`.

### ip

The _IP_ address of the consumer.

### allowed

If the consumer is allowed or not to use the key token (defaults to _True_).


## QuerySet Manager

### allowed

Filter consumers that are allowed to use the associated key (white-listed).

```python
Consumer.objects.allowed()
```

### not_allowed

Filter consumers that are not allowed to use the associated key (black-listed).

```python
Consumer.objects.not_allowed()
```
