from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import UserManager
import datetime
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from base.models import BaseModel
from Store.manager import UserProfileManager
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
import os
from django.core.validators import FileExtensionValidator
# from phonenumber_field.modelfields import PhoneNumberField
# from ckeditor_uploader.fields import RichTextUploadingField

#new
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_image_type(value):
    # Get the file extension
    # _, extension = os.path.splitext(value.name)
    # extension = extension.lower().lstrip('.')

    # Define a whitelist of allowed image types
    allowed_extensions = ['jpeg', 'jpg', 'png']

    # Check if the extension is in the whitelist
    # if extension not in allowed_extensions:
    #     raise ValidationError(f"Unsupported file type: {extension}. Only {', '.join(allowed_extensions)} are allowed.")



class Main_Images(BaseModel):
    cover_image = models.ImageField(upload_to='main_img/',validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    
    
class Logo(BaseModel):
    cover_image = models.ImageField(upload_to='Logo_img/',  validators=[validate_image_type] )
    
    
class Userdp(BaseModel):
    image= models.ImageField(upload_to='user_img/',  validators=[validate_image_type] ) 
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.image)
        super(Userdp, self).save(*args, **kwargs)    
    

class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True, editable=True)
    is_staff = models.BooleanField(default=False)
    # phone_number = models.CharField(max_length=12 , unique=True)
    # is_phone_verified = models.BooleanField(default=False)
    # ootp = models.CharField(max_length=6)
   
    # New field for the user's profile image
    profile_image = models.ImageField(upload_to='profile_images/',  validators=[validate_image_type], blank=True, null=True)

    
    objects = UserProfileManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def _str_(self):
        return self.email

    def get_full_name(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.email)
        super(UserProfile, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.username
 



class Address(models.Model):
   
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_type = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    pincode = models.IntegerField()
    
 
 
class CustomUserManager(UserManager):
     def _create_user(self, email, password, **extra_fields):
         if not email:
             raise ValueError("You have not provided a valid email")
         
    



    


class Category(BaseModel):
    
    name = models.CharField(max_length=150, )
    image = models.ImageField(upload_to='category/', null=True, blank=True, validators=[validate_image_type] )
    # description = models.TextField(max_length=500, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
   
    
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Category, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    

class Sub_Category(BaseModel):
    
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="sub_categories")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Sub_Category, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    
class Product(BaseModel):
          
    description = models.TextField(max_length=500) 
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
    

class Variant(BaseModel):
    SIZE_CHOICES = [
        ('500ml', '500ml'),
        ('1000ml', '1000ml'),
    ]

    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    orginal_price = models.FloatField()
    selling_price = models.FloatField()
    quantity = models.IntegerField()
    cover_image = models.ImageField(upload_to='product/', validators=[validate_image_type] )
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color =models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.color)
  
        super(Variant, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.color
    

class Color_Image(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="colorimages")
    variantimg = models.ImageField(validators=[validate_image_type] )
    

 

class Cart(BaseModel): 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,related_name='cart')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    variant_qty = models.IntegerField(default=1, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    rezor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    rezor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    rezor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
     
    
    
    def save(self, *args, **kwargs):
        self.total_price = self.variant_qty * self.variant.selling_price
        if not self.slug:
            self.slug=slugify(self.variant)
  
        
        super(Cart, self).save(*args, **kwargs)    

  
  
class PromoCode(models.Model):
    code = models.CharField(max_length=10)
    discount_price = models.IntegerField()
    purchase_price = models.IntegerField()
    expaire_date = models.DateField()
    
    
    

    
 
    
class UserOrder(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,related_name='userorder') 
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.FloatField(default=0,null=True)
    payment_mode = models.CharField(max_length=150,null=True)
    status = models.CharField(max_length=150, choices=STATUS_CHOICES, default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length = 150, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
     
    
class UserOrderItem(models.Model):
    order = models.ForeignKey(UserOrder,on_delete=models.CASCADE,related_name='userorderitem')   
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True) 
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=250)
    coupon=models.CharField(max_length=250,null=True)
    
    # def __str__(self):
    #     return '{} - {}'.format(self.order.id, self.order.tracking_no)
         
         

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.pk)         
    
    
