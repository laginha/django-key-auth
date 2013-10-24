'''
Run test:
    python manage.py test app
    python manage.py test app --settings=example.alt_settings
'''
from django.test.client import Client, RequestFactory
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.conf import settings
from keyauth.models import Key, Consumer
from keyauth.consts import HttpResponse401, KEY_AUTH_401_CONTENT, KEY_EXPIRATION_DELTA, KEY_AUTH_401_CONTENT_TYPE
from keyauth.consts import KEY_PARAMETER_NAME, KEY_PATTERN, KEY_AUTH_401_TEMPLATE, KEY_LAST_USED_UPDATE


MIDDLEWARE_CLASSES = getattr(settings, 'MIDDLEWARE_CLASSES') + (
    'keyauth.middleware.KeyRequiredMiddleware',
)


class KeyAuthTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.get_or_create(username='username')[0]
        self.key  = Key.objects.get_or_create(user=self.user)[0]
    
    def assertStatus(self, url, status, kwargs={}):
        response = Client().get(url, kwargs)
        self.assertEqual( response.status_code, status )

    def test_KEY_PARAMETER_NAME(self):
        token_name = KEY_PARAMETER_NAME + 'foo'
        self.assertStatus( '/key_required', 200, {KEY_PARAMETER_NAME: self.key.token} )
        self.assertStatus( '/key_required', 401, {token_name: self.key.token} )
    
    def test_KEY_AUTH_401_CONTENT(self):
        response = Client().get('/key_required')
        if not KEY_AUTH_401_TEMPLATE:
            self.assertEqual( response.content, KEY_AUTH_401_CONTENT )
        self.assertEqual( response.status_code, 401 )
    
    def test_KEY_AUTH_401_CONTENT_TYPE(self):
        response = Client().get('/key_required')
        content_type = response._headers['content-type'][1]
        self.assertEqual( content_type, KEY_AUTH_401_CONTENT_TYPE )
        
    def test_KEY_AUTH_401_TEMPLATE(self):
        response = Client().get('/key_required')
        if KEY_AUTH_401_TEMPLATE:
            self.assertTrue( "<body>" in response.content )
        self.assertEqual( response.status_code, 401 )
    
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
        self.assertStatus( '/key_required', 200, {'key': self.key.token} )
        key = Key.objects.get(id=self.key.id)
        if KEY_LAST_USED_UPDATE:
            self.assertTrue( last_used < key.last_used )
            self.assertEqual( key.activation_date, key.last_used.date() )
        else:
            self.assertEqual( key.activation_date, key.last_used.date() )
            self.assertEqual( last_used, key.last_used )

    def test_key_required(self):
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {'key': self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
    
    @override_settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES)
    def test_KeyRequiredMiddleware(self):
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {'key': self.key.token} )
        self.assertStatus( '/no_key_required', 401 )
    
    def test_authorizarion_logic(self):
        consumer = Consumer.objects.get_or_create(key=self.key, ip='127.0.0.1')[0]
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {'key': self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
        consumer.ip = '1.1.1.1'
        consumer.save()
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 401, {'key': self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
        consumer.delete()
        self.assertStatus( '/key_required', 401 )
        self.assertStatus( '/key_required', 200, {'key': self.key.token} )
        self.assertStatus( '/no_key_required', 200 )
        
