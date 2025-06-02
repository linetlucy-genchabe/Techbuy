from django.db import models
import datetime as dt

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from datetime import timedelta



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description=models.TextField()
    
    
    def __str__(self):
        return self.name


    def save_category(self):
        self.save()

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')  

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # logo = models.ImageField(upload_to='brands/', blank=True, null=True)

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pic = models.ImageField(upload_to= "product_images/")
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save_products(self):
        self.save()
    
    def delete_products(self):
        self.delete()
        
    @classmethod
    def get_allproducts(cls):
        products = cls.objects.all()
        return products
    
# class ProductImage(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
#     pic = models.ImageField(upload_to= "product_images/")
#     angle = models.CharField(max_length=50, blank=True, null=True) 
    

class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True, blank=False, null=False)
    Phonenumber = models.CharField(max_length=15,blank=False , null=False)
    location = models.CharField(max_length=200)
    
    def save_customers(self):
        self.save()
    
    def delete_customers(self):
        self.delete()

class Orders(models.Model):
    Totalprice = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now )
   
    def save_orders(self):
        self.save()
    
    def delete_orders(self):
        self.delete()

# class Cart (models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)


#     def save_cart(self):
#         self.save()
    
#     def delete_cart(self):
#         self.delete()

# CART CLASS WHICH STORES LOGGEDIN USER FROM USER TABLE AND STORES SESSION KEY FOR GUEST USERS AND CLEARD CART AFTER 
# 30 DAYS FOR LOGGED IN USER AND 7 DAYS FOR GUEST USERS.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:  
            if self.user:  
                self.expires_at = timezone.now() + timedelta(days=30)
            else:  
                self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous cart ({self.session_key})"

    def get_items(self):
        return self.items.all()

    def item_count(self):
        return self.items.count()

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def clean_expired(self):
        if timezone.now() > self.expires_at:
            self.delete()
            
     
     
    #CART ITEMS    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        unique_together = ('cart', 'product')


class Reviews(models.Model):
    
    Comment = models.TextField(max_length=1000)
    rating = models.IntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    
    
    def save_reviews(self):
        self.save()
    
    def delete_reviews(self):
        self.delete()
        
    @classmethod
    def get_allreviews(cls):
        reviews = cls.objects.all()
        return reviews
    
    
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
#     session_key = models.CharField(max_length=40, null=True, blank=True)  #Not Logged in  users
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         if self.user:
#             return f"{self.user.username}'s Cart"
#         return f"Session {self.session_key} Cart"

#     def get_total_price(self):
#         return sum(item.get_total_price() for item in self.items.all())
    
    # can Implement functionality to delete items after aperiod of time
    
    # def delete_old_items(self):
    #     expiration = timezone.now() - timedelta(days=14)
    #     self.items.filter(added_at__lt=expiration).delete()
    
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

#     def get_total_price(self):
#         return self.product.price * self.quantity   
