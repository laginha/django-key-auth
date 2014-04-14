'''
Run test:
    python manage.py test app
    python manage.py test app --settings=example.alt_settings
'''
from django.test.client import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission, _user_has_perm
from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings
from django.conf import settings
from keyauth.models import Key, Consumer
from keyauth.consts import KEY_AUTH_401_CONTENT, KEY_EXPIRATION_DELTA, KEY_AUTH_401_CONTENT_TYPE
from keyauth.consts import KEY_PARAMETER_NAME, KEY_PATTERN, KEY_AUTH_401_TEMPLATE, KEY_LAST_USED_UPDATE
from keyauth.consts import KEY_AUTH_403_CONTENT, KEY_AUTH_403_CONTENT_TYPE, KEY_AUTH_403_TEMPLATE, KEY_TYPES


print "Settings:"
print "KEY_PARAMETER_NAME =", KEY_PARAMETER_NAME
print "KEY_PATTERN =", KEY_PATTERN
print "KEY_LAST_USED_UPDATE =", KEY_LAST_USED_UPDATE
print "KEY_EXPIRATION_DELTA =", KEY_EXPIRATION_DELTA
print "KEY_AUTH_401_CONTENT =", KEY_AUTH_401_CONTENT
print "KEY_AUTH_401_CONTENT_TYPE =", KEY_AUTH_401_CONTENT_TYPE
print "KEY_AUTH_401_TEMPLATE =", KEY_AUTH_401_TEMPLATE
print "KEY_AUTH_403_CONTENT =", KEY_AUTH_403_CONTENT
print "KEY_AUTH_403_CONTENT_TYPE =", KEY_AUTH_403_CONTENT_TYPE
print "KEY_AUTH_403_TEMPLATE =", KEY_AUTH_403_TEMPLATE
print "KEY_TYPES = ", KEY_TYPES


MIDDLEWARE_CLASSES = getattr(settings, 'MIDDLEWARE_CLASSES') + (
    'keyauth.middleware.KeyRequiredMiddleware',
)


class KeyAuthTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.get_or_create(username='username')[0]
        self.key  = Key.objects.create(user=self.user)
    
    def assertStatus(self, url, status, kwargs={}):
        response = Client().get(url, kwargs)
        self.assertEqual( response.status_code, status )

    def test_basic_key_required(self):
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 200 )

    def test_authorizarion_logic(self):
        consumer = Consumer.objects.get_or_create(key=self.key, ip='127.0.0.1')[0]
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
        consumer.ip = '1.1.1.1'
        consumer.save()
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 401, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
        consumer.delete()
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 200 )

    #
    # TEST KEY METHODS
    #

    def test_expired_token(self):
        self.key.extend_expiration_date(years=-KEY_EXPIRATION_DELTA-1)
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 401, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 200 )

    def test_extend_expiration_date(self):
        exp_date = self.key.expiration_date
        for i in range(1, 5):
            self.key.extend_expiration_date(years=1)
            delta = self.key.expiration_date - exp_date
            self.assertEqual( delta.days, i*365 )
        
    def test_refresh_token(self):
        token = self.key.token
        self.key.refresh_token()
        self.assertNotEqual( token, self.key.token )
        
    def test_add_consumer(self):
        ip_address = "127.0.0.1"
        self.assertEqual( self.key.consumers.count(), 0 )
        self.key.add_consumer(ip=ip_address)
        self.assertEqual( self.key.consumers.count(), 1 )
        consumer = Consumer.objects.get(key=self.key)
        self.assertTrue( consumer.allowed )
        self.assertEqual( consumer.ip, ip_address )
        
    def test_clear_consumers(self):
        for i in range(1,5):
            self.key.add_consumer(ip="127.0.0."+str(i))
            self.assertEqual( self.key.consumers.count(), i )
        self.key.clear_consumers()
        self.assertEqual( self.key.consumers.count(), 0 )
        
    def test_is_type(self):
        self.assertFalse( self.key.is_type('server') )
        self.assertFalse( self.key.is_type('browser') )
        key  = Key.objects.create(user=self.user, key_type='B')
        self.assertFalse( key.is_type('server') )
        self.assertTrue( key.is_type('browser') )
  
    #
    # TEST PERMISSIONS
    #
        
    def test_has_perm(self):
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(codename='can_read', content_type=content_type)        
        self.assertFalse( self.key.has_perm('auth.can_read') )
        self.key.permissions.add( permission )
        self.assertTrue( self.key.has_perm('auth.can_read') )
    
    def test_has_perm_from_group(self):
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(codename='can_read', content_type=content_type)
        group = Group.objects.create(name='scopename')
        self.assertFalse( self.key.has_perm('auth.can_read') )
        group.permissions.add( permission )
        self.key.groups.add( group )
        self.assertTrue( self.key.has_perm('auth.can_read') )
        
    def test_belongs_to_group(self):
        group = Group.objects.create(name='scopename')
        self.assertFalse( self.key.belongs_to_group('scopename') )
        self.key.groups.add( group )
        self.assertTrue( self.key.belongs_to_group('scopename') )

    def test_perm(self):
        self.assertStatus( '/key_required_with_perm', 401 )
        self.assertStatus( '/key_required_with_perm', 403, {KEY_PARAMETER_NAME: self.key.token} )
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(codename='can_read', content_type=content_type)        
        self.key.permissions.add( permission )
        self.assertStatus( '/key_required_with_perm', 200, {KEY_PARAMETER_NAME: self.key.token} )

    def test_group(self):
        self.assertStatus( '/key_required_with_group', 401 )
        self.assertStatus( '/key_required_with_group', 403, {KEY_PARAMETER_NAME: self.key.token} )
        group = Group.objects.create(name='scopename')
        self.key.groups.add( group )
        self.assertStatus( '/key_required_with_group', 200, {KEY_PARAMETER_NAME: self.key.token} )

    def test_keytype(self):
        self.assertStatus( '/key_required_with_keytype', 401 )
        self.assertStatus( '/key_required_with_keytype', 403, {KEY_PARAMETER_NAME: self.key.token} )
        key  = Key.objects.create(user=self.user, key_type='B')
        self.assertStatus( '/key_required_with_keytype', 200, {KEY_PARAMETER_NAME: key.token} )

    #
    # Managers
    #

    def test_key_manager(self):
        keys = Key.objects.not_expired()
        self.assertTrue( keys.count() )
        self.assertTrue( all(not i.has_expired() for i in keys) )
        self.key.extend_expiration_date(years=-100)
        self.key.save()
        keys = Key.objects.expired()
        self.assertTrue( keys.count() )
        self.assertTrue( all(i.has_expired() for i in keys) )
    
    def test_consumer_manager(self):
        consumer = Consumer.objects.create(key=self.key, ip='127.0.0.1')
        consumers = Consumer.objects.allowed()
        self.assertTrue( consumers.count() )
        self.assertTrue( all(i.allowed for i in consumers) )
        consumer.allowed = False
        consumer.save()
        consumers = Consumer.objects.not_allowed()
        self.assertTrue( consumers.count() )
        self.assertTrue( all(not i.allowed for i in consumers) )
    
    #
    # TEST SETTINGS
    #

    def test_KEY_PARAMETER_NAME(self):
        key_parameter_name = KEY_PARAMETER_NAME + 'foo'
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/key_required', 401, {key_parameter_name: self.key.token} )
    
    def test_KEY_AUTH_401_CONTENT(self):
        response = Client().get('/key_required')
        if not KEY_AUTH_401_TEMPLATE:
            self.assertEqual( response.content, KEY_AUTH_401_CONTENT )
        self.assertEqual( response.status_code, 401 )
    
    def test_KEY_AUTH_403_CONTENT(self):
        response = Client().get('/key_required_with_perm', {KEY_PARAMETER_NAME: self.key.token})
        if not KEY_AUTH_403_TEMPLATE:
            self.assertEqual( response.content, KEY_AUTH_403_CONTENT )
        self.assertEqual( response.status_code, 403 )
    
    def test_KEY_AUTH_401_CONTENT_TYPE(self):
        response = Client().get('/key_required')
        content_type = response._headers['content-type'][1]
        self.assertEqual( content_type, KEY_AUTH_401_CONTENT_TYPE )
    
    def test_KEY_AUTH_403_CONTENT_TYPE(self):
        response = Client().get('/key_required_with_perm', {KEY_PARAMETER_NAME: self.key.token})
        content_type = response._headers['content-type'][1]
        self.assertEqual( content_type, KEY_AUTH_403_CONTENT_TYPE )
    
    def test_KEY_AUTH_401_TEMPLATE(self):
        response = Client().get('/key_required')
        if KEY_AUTH_401_TEMPLATE:
            self.assertTrue( "<body>" in response.content )
        self.assertEqual( response.status_code, 401 )
        
    def test_KEY_AUTH_403_TEMPLATE(self):
        response = Client().get('/key_required_with_perm', {KEY_PARAMETER_NAME: self.key.token})
        if KEY_AUTH_403_TEMPLATE:
            self.assertTrue( "<body>" in response.content )
        self.assertEqual( response.status_code, 403 )
    
    def test_KEY_EXPIRATION_DELTA(self):
        delta = (self.key.expiration_date - self.key.activation_date).days /365
        self.assertEqual( delta, KEY_EXPIRATION_DELTA ) 
                
    def test_KEY_PATTERN(self):
        if KEY_PATTERN == r"[0-9]{3,4}":
            self.assertTrue( all(i.isdigit() for i in self.key.token) )
            self.assertTrue( len(self.key.token) >= 3 )
            self.assertTrue( len(self.key.token) <= 4 )
        else:
            self.assertTrue( len(self.key.token) >= 30 )
            self.assertTrue( len(self.key.token) <= 40 )

    def test_KEY_LAST_USED_UPDATE(self):
        last_used = self.key.last_used
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        key = Key.objects.get(id=self.key.id)
        if KEY_LAST_USED_UPDATE:
            self.assertTrue( last_used < key.last_used )
            self.assertEqual( key.activation_date, key.last_used.date() )
        else:
            self.assertEqual( key.activation_date, key.last_used.date() )
            self.assertEqual( last_used, key.last_used )
            
    def test_KEY_TYPES(self):
        for typechar,typename in KEY_TYPES:
            self.key.is_type( typename )
    
    @override_settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES)
    def test_KeyRequiredMiddleware(self):
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/no_key_required', 401 )  
