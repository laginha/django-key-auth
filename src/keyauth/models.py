from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .consts import KEY_EXPIRATION_DELTA, KEY_PATTERN
import datetime, rstr


def years_from_now(num=KEY_EXPIRATION_DELTA):
    today = datetime.datetime.today()
    delta = datetime.timedelta(days=365*num)
    return (today + delta).date()
    
def generate_token(pattern=KEY_PATTERN):
    return rstr.xeger( pattern )
    
    
class Key(models.Model):
    """
    Key for resource/view access and authentication
    """
    user            = models.ForeignKey(User, related_name='keys')
    # The key token. 
    token           = models.CharField(default=generate_token, max_length=100, unique=True)
    # The date of creation of the key.
    activation_date = models.DateField(auto_now_add=True)
    # The date from which the key will expire, thus no longer valid (by default, one year after creation).
    expiration_date = models.DateField(default=years_from_now)
    # The last time the key was used to access a resource.
    last_used       = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s" %self.token

        
class Consumer(models.Model):
    """
    Web client allowed (or not) to use a key
    
    The client is authorized to access the view:
        - if there is a `Consumer` with the client's *IP* that is explicitly allowed to use the given key,
        - if there is no `Consumer` with a different *IP* explicitly allowed to use the given key
    """
    key     = models.ForeignKey(Key)
    # The *IP* address of the consumer.
    ip      = models.IPAddressField(blank=True)
    # If the consumer is allowed or not to use the key token (defaults to *True*).
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = (("key","ip"),)

    def __unicode__(self):
        text = unicode(self.ip) + u" is%s allowed to use key"
        return text % ( "" if self.allowed else " not")
        

