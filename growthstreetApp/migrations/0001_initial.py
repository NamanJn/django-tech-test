# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=300, verbose_name=b'Reason to borrow')),
                ('amount', models.PositiveIntegerField(verbose_name=b'Amount to borrow')),
                ('loanTime', models.PositiveIntegerField(verbose_name=b'Borrow length time')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userEmail', models.EmailField(max_length=300, verbose_name=b'Email Address')),
                ('userTelephone', models.PositiveIntegerField(verbose_name=b'Contact Number')),
                ('companyNumber', models.PositiveIntegerField(verbose_name=b'companyNumber')),
                ('businessName', models.CharField(max_length=100, verbose_name=b'Business Name')),
                ('businessAddress', models.CharField(max_length=300, verbose_name=b'Business Address')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
