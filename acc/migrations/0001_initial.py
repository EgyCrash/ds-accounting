# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30, blank=True)),
                ('last_name', models.CharField(max_length=30, blank=True)),
                ('lang', models.CharField(max_length=10, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=30, editable=False)),
                ('bill_perm', models.IntegerField(default=0, max_length=1)),
                ('product_perm', models.IntegerField(default=0, max_length=1)),
                ('store_perm', models.IntegerField(default=0, max_length=1)),
                ('customer_perm', models.IntegerField(default=0, max_length=1)),
                ('admin_perm', models.IntegerField(default=0, max_length=1)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('bill_id', models.AutoField(serialize=False, primary_key=True)),
                ('bill_number', models.IntegerField(unique=True, max_length=30, editable=False)),
                ('created_at', models.TimeField(auto_now=True)),
                ('bill_total', models.IntegerField(max_length=30)),
                ('bill_customer', models.CharField(max_length=30)),
                ('bill_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=30, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customer_id', models.AutoField(serialize=False, primary_key=True)),
                ('customer_name', models.CharField(unique=True, max_length=30)),
                ('customer_pic', models.ImageField(upload_to=b'customers_pics', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=30, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('log_id', models.AutoField(serialize=False, primary_key=True)),
                ('log_event', models.CharField(max_length=10, editable=False)),
                ('log_disc', models.CharField(max_length=50, editable=False)),
                ('log_date', models.DateTimeField(auto_now=True)),
                ('log_by', models.CharField(max_length=30, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=30)),
                ('category_disc', models.CharField(max_length=200, blank=True)),
                ('created_by', models.CharField(max_length=30, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(serialize=False, primary_key=True)),
                ('product_name', models.CharField(unique=True, max_length=30)),
                ('product_category', models.CharField(max_length=30)),
                ('product_store', models.CharField(max_length=30)),
                ('product_disc', models.CharField(max_length=200)),
                ('product_pic', models.ImageField(upload_to=b'product_pics', blank=True)),
                ('product_count', models.IntegerField(max_length=30)),
                ('product_price', models.IntegerField(max_length=30)),
                ('product_sell', models.IntegerField(max_length=30)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=30, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('lang', models.CharField(default=b'Arabic', max_length=10)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('status', models.CharField(max_length=5, null=True, blank=True)),
                ('owner', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoldProducts',
            fields=[
                ('sold_id', models.AutoField(serialize=False, primary_key=True)),
                ('bill_number', models.IntegerField(max_length=30, editable=False)),
                ('product_name', models.CharField(max_length=30)),
                ('product_count', models.IntegerField(max_length=30)),
                ('sell_price', models.IntegerField(max_length=30)),
                ('total', models.IntegerField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoreCategories',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=30)),
                ('category_disc', models.CharField(max_length=200, blank=True)),
                ('created_by', models.CharField(max_length=30, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('store_id', models.AutoField(serialize=False, primary_key=True)),
                ('store_name', models.CharField(unique=True, max_length=30)),
                ('store_category', models.CharField(max_length=30)),
                ('store_address', models.CharField(max_length=100)),
                ('store_disc', models.CharField(default=None, max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=30, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
