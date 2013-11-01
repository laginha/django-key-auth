from django.db import models
from datetime import date


class KeyQuerySet(models.query.QuerySet):
    
    def expired(self):
        return self.filter(expiration_date__lt=date.today())
    
    def not_expired(self):
        return self.filter(expiration_date__gte=date.today())
        

class ConsumerQuerySet(models.query.QuerySet):
    
    def allowed(self):
        return self.filter(allowed=True)
    
    def not_allowed(self):
        return self.filter(allowed=False)
