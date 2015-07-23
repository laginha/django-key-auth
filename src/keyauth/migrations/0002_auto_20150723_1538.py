# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
