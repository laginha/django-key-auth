from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from model_utils.managers import PassThroughManager
from .consts import KEY_EXPIRATION_DELTA, KEY_PATTERN
from .managers import ConsumerQuerySet, KeyQuerySet
import datetime, rstr

def timedelta_years(years):
    return datetime.timedelta(days=365*years)
    
def years_from_now(num=KEY_EXPIRATION_DELTA):
    today = datetime.datetime.today()
    delta = timedelta_years(num)
    return (today + delta).date()
    
def generate_token(pattern=KEY_PATTERN):
    return rstr.xeger( pattern )
    
    
class Key(models.Model):
    """
    Key for resource/view access and authentication
    """
    objects = PassThroughManager.for_queryset_class(KeyQuerySet)()
    
    groups          = models.ManyToManyField(Group)
    permissions     = models.ManyToManyField(Permission)
    user            = models.ForeignKey(User, related_name='keys')
    # The key token. 
    token           = models.CharField(default=generate_token, max_length=100, unique=True)
    # The date of creation of the key.
    activation_date = models.DateField(auto_now_add=True)
    # The date from which the key will no longer be valid (by default, one year after creation).
    expiration_date = models.DateField(default=years_from_now)
    # The last time the key was used to access a resource.
    last_used       = models.DateTimeField(auto_now=True)

    def has_expired(self):
        """
        Checks if key has expired its validation date
        """
        return datetime.date.today() > self.expiration_date
    
    def extend_expiration_date(self, years=1):
        """
        Extend expiration date a number of given years
        """
        delta = timedelta_years(years)
        self.expiration_date = self.expiration_date + delta
        self.save()
        
    def refresh_token(self, pattern=KEY_PATTERN):
        """
        Replace token with a new generated one
        """
        self.token = generate_token(pattern)
        self.save()
    
    def add_consumer(self, ip):
        """
        Add consumer based on its ip address
        """
        Consumer.objects.get_or_create(key=self, ip=ip)
    
    def clear_consumers(self):
        """
        Remove all consumers
        """
        self.consumers.all().delete()
    
    def get_consumers(self):
        """
        Get all consumers with key
        """
        return self.consumers.all()
    
    def has_perm(self, perm):
        """
        Checks if key has the given django's auth Permission
        """
        if '.' in perm:
            app_label, codename = perm.split('.')
            permissions = self.permissions.filter(
                content_type__app_label = app_label, 
                codename = codename)
            groups = self.groups.filter(
                permissions__content_type__app_label = app_label,
                permissions__codename = codename )
        else:
            permissions = self.permissions.filter(codename = perm)
            groups = self.groups.filter(permissions__codename = perm)
        return permissions.exists() or groups.exists()         
    
    def belongs_to_group(self, name):
        """
        Checks if key belongs to a django's auth Group
        """
        return self.groups.filter(name=name).exists()
    
    def __unicode__(self):
        return u"%s" %self.token

        
class Consumer(models.Model):
    """
    Web client allowed (or not) to use a key
    """
    objects = PassThroughManager.for_queryset_class(ConsumerQuerySet)()
    
    key     = models.ForeignKey(Key, related_name="consumers")
    # The *IP* address of the consumer.
    ip      = models.IPAddressField(blank=True)
    # If the consumer is allowed or not to use the key token (defaults to *True*).
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = (("key","ip"),)

    def __unicode__(self):
        text = unicode(self.ip) + u" is%s allowed to use key"
        return text % ( "" if self.allowed else " not")
        

