# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from acc.forms import *
from django.core import serializers
from acc.models import  *
import time
try:
    from django.utils import simplejson as json
except:
    import simplejson as json

def site_settings(request):
    if SiteSettings.objects.filter(id=1):
        site = SiteSettings.objects.get(id=1)
        title = site.title
        with open('acc/lang.json') as data_file:
            langs = json.load(data_file)
            user = request.user.username
            default = SiteSettings.objects.get(id=1)
            default_lang = default.lang
            if request.user.is_anonymous():
                lang = langs[default_lang]
                return {"Title":title, "Lang":lang }
            elif user:
                lang = request.user.lang
                if lang:
                    lang = langs[lang]
                    return {"Title": title, "Lang": lang }
                else:
                    lang = langs['English']
                    return {"Title": title, "Lang": lang }
    else:
        with open('acc/lang.json') as data_file:
            langs = json.load(data_file)
            lang = langs['English']
            title = 'Digital Solutions Accounting System'
            return {"Title": title, "Lang": lang }

def user_login (request):
    settings = site_settings(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            user_info = authenticate(username=username, password=password)
            if user_info is not None:
                if user_info.is_active:
                    login(request, user_info)
                    thenext = request.POST['Next_Page']
                    if thenext != 'None':
                        return HttpResponseRedirect(thenext)
                    else:
                        return HttpResponseRedirect('/')
                else :
                    message = settings['Lang']['user_not_active']
                    form = LoginForm()
                    return render(request, 'login.html', {'form': form, 'ErrorMessage': message, 'Settings': settings})
            else:
                message = settings['Lang']['user_error']
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'ErrorMessage': message, 'Settings': settings})
    else:
        form = LoginForm()
        next_page = request.GET.get('next')
    return render(request, 'login.html',{'form':form,'Next_Page':next_page, 'Settings': settings})

@login_required
def index(request):
    settings = site_settings(request)
    return  render(request,'index.html', {'Settings': settings})


####################Products Functions  ##############################

def product_add(request):
     settings = site_settings(request)
     categories = ProductCategories.objects.order_by('category_id')
     stores = Stores.objects.order_by('store_id')
     perm = request.user.product_perm
     admin_perm = request.user.admin_perm
     if perm is 1 or perm is 7 or admin_perm is 7:
         if request.POST:
            form = ProductAdd(request.POST)
            if form.is_valid():
                product_name = form.cleaned_data['product_name']
                check = Products.objects.filter(product_name=product_name)
                if check:
                    error_message = settings['Lang']['name_exist']
                    form = ProductAdd()
                    return render(request, 'addproduct.html', {'ErrorMessage': error_message, 'Categories': categories, 'form': form, 'Stores': stores, 'Settings': settings})
                else:
                    product_name = form.cleaned_data['product_name']
                    product_disc = form.cleaned_data['product_disc']
                    #product_pic = form.cleaned_data['product_pic']
                    product_category = request.POST['product_category']
                    product_store = request.POST['product_store']
                    product_price = form.cleaned_data['product_price']
                    product_sell = form.cleaned_data['product_sell']
                    product_count = form.cleaned_data['product_count']
                    Products.objects.create(
                        product_name=product_name,
                        product_disc=product_disc,
                        #product_pic = product_pic,
                        product_category=product_category,
                        product_store=product_store,
                        product_price=product_price,
                        product_sell=product_sell,
                        product_count=product_count,
                        created_by=request.user.username,
                    )
                    Logs.objects.create(
                        log_event='Create',
                        log_disc='Product '+product_name,
                        log_by=request.user.username,
                    )
                    message = settings['Lang']['add_success']
                    form = ProductAdd()
                    return render(request, 'addproduct.html', {'Message': message,'Categories': categories,'form':form, 'Stores': stores, 'Settings': settings})
            else:
                error_message = settings['Lang']['error']
                form = ProductAdd()
                return render(request, 'addproduct.html', {'ErrorMessage': error_message,'Categories': categories,'form':form, 'Stores': stores, 'Settings': settings})
         else:
            form = ProductAdd()
         return render(request, 'addproduct.html', {'form': form,'Categories': categories, 'Stores': stores, 'Settings': settings})
     else:
         error_message =settings['Lang']['no_perm']
         return render(request, 'viewproduct.html', {'ErrorMessage':error_message, 'Settings': settings})

def product_view(request, product_id):
     perm = request.user.product_perm
     admin_perm = request.user.admin_perm
     settings = site_settings(request)
     if perm is 1 or perm is 7 or admin_perm is 7:
        if product_id == "all":
            products = Products.objects.order_by('product_id')
            return render(request,'viewproduct.html',{'Products':products, 'Settings': settings})
        else :
             product = Products.objects.filter(product_id=product_id)
             if product :
                 product = Products.objects.get(product_id=product_id)
                 return render(request,'viewproduct.html',{
                    'product_id':product.product_id,
                    'product_name':product.product_name,
                    'product_category':product.product_category,
                    'product_store':product.product_store,
                    'product_count':product.product_count,
                    'product_price':product.product_price,
                    'product_sell':product.product_sell,
                    'created_at':product.created_at,
                    'created_by':product.created_by,
                    'Settings': settings
                 })
             error_message =settings['Lang']['does_not_exist']
             return render(request, 'viewproduct.html', {'ErrorMessage':error_message, 'Settings': settings})
     else:
         error_message =settings['Lang']['no_perm']
         return render(request, 'viewproduct.html', {'ErrorMessage':error_message, 'Settings': settings})

def product_delete( request, product_id):
     perm = request.user.product_perm
     admin_perm = request.user.admin_perm
     if perm is 4 or perm is 7 or admin_perm is 7:
        settings = site_settings(request)
        delete = Products.objects.filter(product_id=product_id)
        if delete:
            delete = Products.objects.get(product_id=product_id)
            Logs.objects.create(
                log_event='Delete',
                log_disc='Product  '+delete.product_name,
                log_by=request.user.username
            )
            delete.delete()
            Message =settings['Lang']['deleted']
            return JsonResponse({'Message': Message})
        else :
            Message =settings['Lang']['does_not_exist']
            return JsonResponse({'Message': Message})

####################Product Categories Functions  ##############################

def product_category_add(request):
     settings = site_settings(request)
     #setting = {'Settings':settings}
     if request.POST:
        form = ProductCategoryAdd(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            check = ProductCategories.objects.filter(category_name=category_name)
            if check:
                error_message = settings['Lang']['name_exist']
                form = ProductCategoryAdd()
                return render(request, 'addproductcategory.html', {'ErrorMessage': error_message,'form': form, 'Settings': settings})
            else:
                category_name = form.cleaned_data['category_name']
                category_disc= form.cleaned_data['category_disc']
                ProductCategories.objects.create(
                    category_name = category_name,
                    category_disc = category_disc,
                    created_by = request.user.username,
                )
                Logs.objects.create(
                    log_event='Delete',
                    log_disc='Product Category '+category_name,
                    log_by=request.user.username
                )
                message = settings['Lang']['add_success']
                form = ProductCategoryAdd()
                return render(request, 'addproductcategory.html', {'Message': message,'form': form, 'Settings': settings})
        else:
            error_message = settings['Lang']['error']
            form = ProductCategoryAdd()
            return render(request, 'addproductcategory.html', {'ErrorMessage': error_message,'form': form, 'Settings': settings})
     else:
        form = ProductCategoryAdd()
        return render(request, 'addproductcategory.html', {'form': form, 'Settings': settings})

def product_category_view(request, category_id):
    settings = site_settings(request)
    if category_id == "all":
        categories = ProductCategories.objects.order_by('category_id')
        return render(request,'viewproductcategory.html',{'Categories':categories, 'Settings': settings})
    else :
         category = ProductCategories.objects.filter(category_id=category_id)
         if category:
             category = ProductCategories.objects.get(category_id=category_id)
             return render(request,'viewproductcategory.html',{
                'category_id':category.category_id,
                'category_name':category.category_name,
                'created_by':category.created_by,
                'Settings': settings
             })
         else:
            error_message = settings['Lang']['does_not_exist']
            return render(request, 'viewproductcategory.html', {'ErrorMessage':error_message, 'Settings': settings})


def product_category_delete( request, category_id):
    settings = site_settings(request)
    delete = ProductCategories.objects.filter(category_id=category_id)
    if delete:
        delete = ProductCategories.objects.get(category_id=category_id)
        Logs.objects.create(
            log_event='Delete',
            log_disc='Product Category '+delete.category_name,
            log_by=request.user.username
        )
        delete.delete()
        message = settings['Lang']['deleted']
        return JsonResponse({'Message': message})
    else :
        message = settings['Lang']['does_not_exist']
        return JsonResponse({'Message': message})

#################### Customers Functions  ##############################

def customer_add(request):
     settings = site_settings(request)
     if request.POST:
        form = CustomerAdd(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            check = Customers.objects.filter(customer_name=customer_name)
            if check:
                error_message = settings['Lang']['name_exist']
                form = CustomerAdd()
                return render(request, 'addcustomer.html', {'ErrorMessage': error_message,'form': form, 'Settings': settings})
            else:
                customer_name = form.cleaned_data['customer_name']
                Customers.objects.create(
                    customer_name=customer_name,
                    created_by=request.user.username,
                )
                Logs.objects.create(
                    log_event='Create',
                    log_disc='Customer '+customer_name,
                    log_by=request.user.username
                )
                message = settings['Lang']['add_success']
                form = CustomerAdd()
                return render(request, 'addcustomer.html', {'Message': message,'form': form, 'Settings': settings})
        else:
            error_message =settings['Lang']['error']
            form = CustomerAdd()
            return render(request, 'addcustomer.html', {'ErrorMessage': error_message,'form': form, 'Settings': settings})
     else:
        form = CustomerAdd()
        return render(request, 'addcustomer.html', {'form': form, 'Settings': settings})


def customer_view(request, customer_id):
    settings = site_settings(request)
    if customer_id == "all":
        customers = Customers.objects.order_by('customer_id')
        return render(request,'viewcustomer.html',{'Customers':customers, 'Settings': settings})
    else :
         customer = Customers.objects.filter(customer_id=customer_id)
         if customer:
             customer = Customers.objects.get(customer_id=customer_id)
             return render(request,'viewcustomer.html',{
                'customer_id':customer.customer_id,
                'customer_name':customer.customer_name,
                'created_by':customer.created_by,
                'created_at':customer.created_at,
             })
         else:
             error_message =settings['Lang']['does_not_exist']
             return render(request, 'viewcustomer.html', {'ErrorMessage':error_message, 'Settings': settings})


def customer_delete( request, customer_id):
    settings = site_settings(request)
    delete = Customers.objects.filter(customer_id=customer_id)
    if delete:
        delete = Customers.objects.get(customer_id=customer_id)
        Logs.objects.create(
            log_event='Delete',
            log_disc='Customer '+delete.customer_name,
            log_by=request.user.username
        )
        delete.delete()
        Message =settings['Lang']['deleted']
        return JsonResponse({'Message': Message})
    else :
        Message = settings['Lang']['error']
        return JsonResponse({'Message': Message})

#################### Store Functions ###################
def store_category_add(request):
     settings = site_settings(request)
     if request.POST:
        form = StoreCategoryAdd(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            check = StoreCategories.objects.filter(category_name=category_name)
            if check:
                error_message = settings['Lang']['name_exist']
                form = StoreCategoryAdd()
                return render(request, 'addstorecategory.html', {'ErrorMessage': error_message,'form': form, 'Settings': settings})
            else:
                category_name = form.cleaned_data['category_name']
                category_disc= form.cleaned_data['category_disc']
                StoreCategories.objects.create(
                    category_name=category_name,
                    category_disc=category_disc,
                    created_by=request.user.username,
                )
                Logs.objects.create(
                    log_event='Create',
                    log_disc='Store Category '+category_name,
                    log_by=request.user.username
                )
                message = settings['Lang']['add_success']
                form = StoreCategoryAdd()
                return render(request, 'addstorecategory.html', {'Message': message,'form': form, 'Settings': settings})
        else:
            error_message = settings['Lang']['error']
            form = StoreCategoryAdd()
            return render(request, 'addstorecategory.html', {'ErrorMessage': error_message, 'form': form, 'Settings': settings })
     else:
        form = StoreCategoryAdd()
        return render(request, 'addstorecategory.html', {'form': form, 'Settings': settings})

def store_category_view(request, category_id):
    settings = site_settings(request)
    if category_id == "all":
        categories = StoreCategories.objects.order_by('category_id')
        return render(request,'viewstorecategory.html',{'Categories':categories, 'Settings': settings})
    else :
         category = StoreCategories.objects.filter(category_id=category_id)
         if category:
             category  =StoreCategories.objects.get(category_id=category_id)
             return render(request,'viewstorecategory.html',{
                'category_id':category.category_id,
                'category_name':category.category_name,
                'created_by':category.created_by,
                'Settings': settings
             })
         else:
            error_message = settings['Lang']['does_not_exist']
            return render(request, 'viewstorecategory.html', {'ErrorMessage':error_message, 'Settings': settings})

def store_category_delete( request, category_id):
    settings = site_settings(request)
    delete = StoreCategories.objects.filter(category_id=category_id)
    if delete:
        delete = StoreCategories.objects.get(category_id=category_id)
        Logs.objects.create(
            log_event='Delete',
            log_disc='Store Category '+delete.category_name,
            log_by=request.user.username,
        )
        delete.delete()
        Message = settings['Lang']['deleted']
        return JsonResponse({'Message': Message})
    else :
        Message = settings['Lang']['does_not_exist']
        return JsonResponse({'Message': Message})

def store_add(request):
     settings = site_settings(request)
     categories = StoreCategories.objects.order_by('category_id')
     if request.POST:
        form = StoreAdd(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            check = Stores.objects.filter(store_name=store_name)
            if check:
                error_message = settings['Lang']['name_exist']
                form = StoreAdd()
                return render(request, 'addstore.html', {'ErrorMessage': error_message, 'Categories': categories,'form':form, 'Settings': settings})
            else:
                store_name = form.cleaned_data['store_name']
                store_category = form.cleaned_data['store_category']
                store_address = form.cleaned_data['store_address']
                store_disc = form.cleaned_data['store_disc']
                Stores.objects.create(
                    store_name=store_name,
                    store_category=store_category,
                    store_address=store_address,
                    store_disc=store_disc,
                    created_by=request.user.username,
                )
                Logs.objects.create(
                    log_event='Create',
                    log_disc='Store '+store_name,
                    log_by=request.user.username,
                )
                message = settings['Lang']['add_success']
                form = StoreAdd()
                return render(request, 'addstore.html', {'Message': message,'Categories': categories,'form':form, 'Settings': settings})
        else:
            error_message =settings['Lang']['error']
            form = StoreAdd()
            return render(request, 'addstore.html', {'ErrorMessage': error_message,'Categories': categories,'form':form, 'Settings': settings})
     else:
        form = StoreAdd()
     return render(request, 'addstore.html', {'form': form,'Categories': categories, 'Settings': settings})

def store_delete( request, store_id):
    settings = site_settings(request)
    delete = Stores.objects.filter(store_id=store_id)
    if delete:
        delete = Stores.objects.get(store_id=store_id)
        Logs.objects.create(
            log_event='Delete',
            log_disc='Store  '+delete.store_name,
            log_by=request.user.username,
        )
        delete.delete()
        message = settings['Lang']['deleted']
        return JsonResponse({'Message': message})
    else :
        message = settings['Lang']['does_not_exist']
        return JsonResponse({'Message': message})

def store_view(request, store_id):
    settings = site_settings(request)
    if store_id == "all":
        stores = Stores.objects.order_by('store_id')
        return render(request,'viewstore.html',{'Stores':stores, 'Settings': settings})
    else :
         store = Stores.objects.filter(store_id=store_id)
         if store:
             store  =Stores.objects.get(store_id=store_id)
             products = Products.objects.filter(product_store=store.store_name)
             return render(request,'viewstore.html',{
                'store_id':store.store_id,
                'store_name':store.store_name,
                'store_disc':store.store_disc,
                'store_address':store.store_address,
                'created_by':store.created_by,
                'created_at':store.created_at,
                'store_category':store.store_category,
                 'Products':products,
             })
         else:
            error_message = settings['Lang']['does_not_exist']
            return render(request, 'viewstore.html', {'ErrorMessage':error_message, 'Settings': settings})

##################Log Functions #######################

def log(request):
    settings = site_settings(request)
    logs = Logs.objects.order_by('-log_id')
    return render(request, 'log.html', {'Logs': logs, 'Settings': settings})

################## Bill Functions ######################

def auto_complete_product(request):
   search = request.GET['term']
   products = Products.objects.all().filter(product_name__startswith=search)
   products_serialized = serializers.serialize('json', products)
   return JsonResponse(products_serialized, safe=False)

def auto_complete_customer(request):
   search = request.GET['term']
   customers = Customers.objects.all().filter(customer_name__startswith=search)
   customers_serialized = serializers.serialize('json', customers)
   return JsonResponse(customers_serialized, safe=False)


def add_bill(request):
    settings = site_settings(request)
    bill_id = time.strftime("%Y%m%d%H%M%S")
    if request.POST:
        for i in range(1, 51):
            product = 'product_' + str(i)
            sell = 'sell_' + str(i)
            count = 'count_' + str(i)
            total = 'total_' + str(i)
            if product and sell and count and total in request.POST.keys():
                product = request.POST[product]
                sell = request.POST[sell]
                count = request.POST[count]
                total = request.POST[total]
                SoldProducts.objects.create(
                    bill_number=request.POST['bill_id'],
                    product_name=product,
                    product_count=count,
                    sell_price=sell,
                    total=total,
                )
        Bills.objects.create(
            bill_number=request.POST['bill_id'],
            bill_total=request.POST['all_total'],
            bill_customer=request.POST['customer_name'],
            created_by=request.user.username,
        )
        Logs.objects.create(
            log_event='Create',
            log_disc='Bill  '+request.POST['bill_id'],
            log_by=request.user.username,
        )
        message = settings['Lang']['add_success']
        return render(request, 'addbill.html', {'Settings': settings, 'Message': message, 'Bill_ID': bill_id})
    else:
        return render(request, 'addbill.html', {'Settings': settings, 'Bill_ID': bill_id})

################## Admin Control Panel #################

def admincp(request):
    settings = site_settings(request)
    admin_perm = request.user.admin_perm
    users = UserModel.objects.order_by('id')
    if admin_perm is 7:
        if request.POST:
            profile_form = UserEdit(request.POST)
            site_form = SiteSettingsForm(request.POST)
            new_user = UserAdd(request.POST)
            if 'profile_btn' in request.POST:
                if profile_form.is_valid():
                    username = request.user.username
                    if username:
                        email = profile_form.cleaned_data['email']
                        bill_perm = profile_form.cleaned_data['bill_perm']
                        product_perm = profile_form.cleaned_data['product_perm']
                        store_perm = profile_form.cleaned_data['store_perm']
                        customer_perm = profile_form.cleaned_data['customer_perm']
                        admin_perm = profile_form.cleaned_data['admin_perm']
                        first_name = profile_form.cleaned_data['first_name']
                        last_name = profile_form.cleaned_data['last_name']
                        lang = request.POST['lang']
                        edit = UserModel.objects.get(username=username)
                        edit.email = email
                        edit.bill_perm = bill_perm
                        edit.product_perm = product_perm
                        edit.store_perm = store_perm
                        edit.customer_perm = customer_perm
                        edit.admin_perm = admin_perm
                        edit.lang = lang
                        edit.first_name = first_name
                        edit.last_name = last_name
                        edit.save()
                        message = settings['Lang']['edited_success']
                        profile_form = UserEdit()
                        site_form = SiteSettingsForm()
                        return render(request, 'admincp.html', {'Message': message, 'profile_form': profile_form, 'site_form':site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
                    else:
                        error_message = settings['Lang']['error']
                        profile_form = UserEdit()
                        site_form = SiteSettingsForm()
                        new_user = UserAdd()
                        return render(request, 'admincp.html', {'ErrorMessage': error_message, 'profile_form': profile_form, 'site_form':site_form , 'new_user':new_user, 'Settings': settings, 'Users':users})
                else:
                    error_message = settings['Lang']['error']+2
                    profile_form = UserEdit()
                    site_form = SiteSettingsForm()
                    new_user = UserAdd()
                    return render(request, 'admincp.html', {'ErrorMessage': error_message, 'profile_form': profile_form, 'site_form':site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
            elif 'site_btn' in request.POST:
                if site_form.is_valid():
                    username = request.user.username
                    site_vars = SiteSettings.objects.filter(id=1)
                    if site_vars:
                        if username:
                            email = site_form.cleaned_data['email']
                            owner = site_form.cleaned_data['owner']
                            status = request.POST['sitestatus']
                            title = site_form.cleaned_data['title']
                            edit = SiteSettings.objects.get(id=1)
                            edit.email = email
                            edit.title = title
                            edit.status = status
                            edit.owner = owner
                            edit.save()
                            message = settings['Lang']['edited_success']
                            profile_form = UserEdit()
                            site_form = SiteSettingsForm()
                            new_user = UserAdd()
                            return render(request, 'admincp.html', {'Message': message, 'profile_form': profile_form, 'site_form': site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
                        else:
                            error_message = settings['Lang']['error']
                            profile_form = UserEdit()
                            site_form = SiteSettingsForm()
                            new_user = UserAdd()
                            return render(request, 'admincp.html', {'ErrorMessage': error_message, 'profile_form': profile_form, 'site_form': site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
                    else:
                        email = profile_form.cleaned_data['email']
                        owner = profile_form.cleaned_data['owner']
                        status = request.POST['sitestatus']
                        lang = request.POST['lang']
                        title = profile_form.cleaned_data['title']
                        SiteSettings.objects.create(
                            email = email,
                            owner = owner,
                            status = status,
                            title = title,
                            lang = lang,
                        )
                        message = settings['Lang']['edited_success']
                        profile_form = UserEdit()
                        site_form = SiteSettingsForm()
                        new_user = UserAdd()
                        return render(request, 'admincp.html', {'Message': message , 'profile_form': profile_form, 'site_form': site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
            elif 'new_user_btn' in request.POST:
                if new_user.is_valid():
                    username = new_user.cleaned_data['username']
                    password = new_user.cleaned_data['password']
                    email = new_user.cleaned_data['email']
                    bill_perm = new_user.cleaned_data['bill_perm']
                    product_perm = new_user.cleaned_data['product_perm']
                    store_perm = new_user.cleaned_data['store_perm']
                    customer_perm = new_user.cleaned_data['customer_perm']
                    admin_perm = new_user.cleaned_data['admin_perm']
                    first_name = new_user.cleaned_data['first_name']
                    last_name = new_user.cleaned_data['last_name']
                    lang = request.POST['lang']
                    UserModel.objects.create(
                        username=username,
                        email=email,
                        bill_perm=bill_perm,
                        product_perm=product_perm,
                        store_perm=store_perm,
                        customer_perm=customer_perm,
                        admin_perm=admin_perm,
                        first_name=first_name,
                        last_name=last_name,
                        lang=lang,
                        created_by=request.user.username,
                    )
                    user = UserModel.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    message = settings['Lang']['add_success']
                    profile_form = UserEdit()
                    site_form = SiteSettingsForm()
                    new_user=UserAdd()
                    return render(request, 'admincp.html', {'Message': message, 'profile_form': profile_form, 'site_form':site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
                else:
                    error_message = settings['Lang']['error']
                    profile_form = UserEdit()
                    site_form = SiteSettingsForm()
                    new_user = UserAdd()
                    return render(request, 'admincp.html', {'ErrorMessage': error_message, 'profile_form': profile_form, 'site_form':site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
        else:
            profile_form = UserEdit()
            site_form = SiteSettingsForm()
            new_user = UserAdd()
            return render(request, 'admincp.html', {'profile_form': profile_form, 'site_form': site_form, 'new_user':new_user, 'Settings': settings, 'Users':users})
    else:
        error_message = settings['Lang']['no_perm']
        return render(request, 'admincp.html', {'ErrorMessage': error_message,'Settings': settings})

def user_logout(request):
        logout(request)
        return HttpResponseRedirect('/login/')