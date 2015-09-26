from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ProductCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True,max_length=30)
    category_disc = models.CharField(max_length=200, blank=True)
    created_by = models.CharField(max_length=30, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

class StoreCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True,max_length=30)
    category_disc = models.CharField(max_length=200, blank=True)
    created_by = models.CharField(max_length=30, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30, unique=True)
    product_category = models.CharField(max_length=30)
    product_store = models.CharField(max_length=30)
    product_disc = models.CharField(max_length=200)
    product_pic = models.ImageField(upload_to='product_pics', blank=True)
    product_count = models.IntegerField(max_length=30)
    product_price = models.IntegerField(max_length=30)
    product_sell = models.IntegerField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=30, editable=False)

class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(unique=True, max_length=30)
    customer_pic = models.ImageField(upload_to='customers_pics', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=30, editable=False)

class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_number = models.IntegerField(max_length=30, editable=False, unique=True)
    created_at = models.TimeField(auto_now=True, editable=False)
    bill_total = models.IntegerField(max_length=30)
    bill_customer = models.CharField(max_length=30)
    bill_modified = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.CharField(max_length=30, editable=False)

class SoldProducts(models.Model):
    sold_id = models.AutoField(primary_key=True)
    bill_number = models.IntegerField(max_length=30, editable=False)
    product_name = models.CharField(max_length=30)
    product_count = models.IntegerField(max_length=30)
    sell_price = models.IntegerField(max_length=30)
    total = models.IntegerField(max_length=30)

class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    log_event = models.CharField(max_length=10, editable=False)
    log_disc = models.CharField(max_length=50, editable=False)
    log_date = models.DateTimeField(auto_now=True, editable=False)
    log_by = models.CharField(max_length=30, editable=False)

class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(unique=True, max_length=30)
    store_category = models.CharField( max_length=30)
    store_address = models.CharField(max_length=100)
    store_disc = models.CharField(max_length=200, default=None)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.CharField(max_length=30, editable=False)

class UserModelManager(BaseUserManager):
    def create_user(self, email, username,admin_perm,
                    password):
        user = self.model(email=email,
                          username= username, admin_perm=admin_perm)
        user .set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email,admin_perm,
                         password,username):
        user = self.create_user(email=email, username=username,
                                password=password, admin_perm=admin_perm)
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    lang = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.CharField(max_length=30, editable=False)
    bill_perm = models.IntegerField(max_length=1, default=0)
    product_perm = models.IntegerField(max_length=1, default=0)
    store_perm = models.IntegerField(max_length=1, default=0)
    customer_perm = models.IntegerField(max_length=1, default=0)
    admin_perm = models.IntegerField(max_length=1, default=0)
    objects = UserModelManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'admin_perm']

class  SiteSettings(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    lang = models.CharField(max_length=10,default="Arabic")
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=5, blank=True, null=True)
    owner = models.CharField(max_length=30, blank=True, null=True)