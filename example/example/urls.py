from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^key_required$', 'app.views.view_key_required', name='key'),
    url(r'^key_required_with_group$', 'app.views.view_key_required_with_group', name='key-with-group'),
    url(r'^key_required_with_perm$', 'app.views.view_key_required_with_perm', name='key-with-perm'),
    url(r'^key_required_with_keytype$', 'app.views.view_key_required_with_keytype', name='key-with-keytype'),
    url(r'^no_key_required$', 'app.views.view_key_not_required', name='no-key'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
