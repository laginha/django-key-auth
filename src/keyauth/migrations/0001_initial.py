# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import keyauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField(blank=True)),
                ('allowed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=keyauth.models.generate_token, unique=True, max_length=100)),
                ('activation_date', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField(default=keyauth.models.days_from_now)),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('key_type', models.CharField(max_length=1, choices=[(b'S', b'server'), (b'B', b'browser')])),
                ('groups', models.ManyToManyField(to='auth.Group')),
                ('permissions', models.ManyToManyField(to='auth.Permission')),
                ('user', models.ForeignKey(related_name='keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='consumer',
            name='key',
            field=models.ForeignKey(related_name='consumers', to='keyauth.Key'),
        ),
        migrations.AlterUniqueTogether(
            name='consumer',
            unique_together=set([('key', 'ip')]),
        ),
    ]
