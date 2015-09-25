# -*- coding: UTF-8 -*-
from django import forms
import autocomplete_light

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=30,required=True)
    Password = forms.CharField(max_length=30,required=True,widget=forms.PasswordInput)


class ProductAdd(forms.Form):
    product_name = forms.CharField(max_length=30, required=True)
    product_disc = forms.CharField(max_length=200)
    #product_pic = forms.FileField()
    product_category = forms.CharField(max_length=30, required=True)
    product_count = forms.IntegerField( required=True)
    product_price = forms.IntegerField( required=True)
    product_sell = forms.IntegerField( required=True)

class ProductCategoryAdd(forms.Form):
    category_name = forms.CharField(max_length=30, required=True)
    category_disc = forms.CharField(max_length=200)

class CustomerAdd(forms.Form):
    customer_name = forms.CharField(max_length=30, required=True)
    #customer_pic = forms.FileField()

class BillAdd(forms.Form):
    bill_total = forms.IntegerField( required=True)
    bill_customer = forms.CharField(max_length=30, required=True)

class StoreCategoryAdd(forms.Form):
    category_name = forms.CharField(max_length=30, required=True)
    category_disc = forms.CharField(max_length=200)

class StoreAdd(forms.Form):
    store_name = forms.CharField(max_length=30, required=True)
    store_category = forms.CharField( max_length=30)
    store_address = forms.CharField(max_length=100)
    store_disc = forms.CharField(max_length=200)

class UserEdit(forms.Form):
    email = forms.EmailField(max_length=30,required=True)
    bill_perm = forms.IntegerField(max_value=7, required=True)
    product_perm = forms.IntegerField(max_value=7, required=True)
    store_perm = forms.IntegerField(max_value=7, required=True)
    customer_perm = forms.IntegerField(max_value=7, required=True)
    admin_perm = forms.IntegerField(max_value=7, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

class UserAdd(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30,required=True,widget=forms.PasswordInput)
    email = forms.EmailField(max_length=30,required=True)
    bill_perm = forms.IntegerField(max_value=7, required=True)
    product_perm = forms.IntegerField(max_value=7, required=True)
    store_perm = forms.IntegerField(max_value=7, required=True)
    customer_perm = forms.IntegerField(max_value=7, required=True)
    admin_perm = forms.IntegerField(max_value=7, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

class SiteSettingsForm(forms.Form):
    title = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(required=False)
    owner = forms.CharField(max_length=30,required=False)