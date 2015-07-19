# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growthstreetApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='businessSector',
            field=models.CharField(default=b'boolean', max_length=100, null=True, verbose_name=b'Business Sector', choices=[(b'Retail', b'Retail'), (b'Professional', b'Professional Services'), (b'Food', b'Food & Drink'), (b'Entertainment', b'Entertainment')]),
        ),
    ]
