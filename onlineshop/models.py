from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    
    def __str__(self):
        return self.name


    def save_category(self):
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
   
    # description = models.TextField(blank=True)

    def save_profile(self):
        self.save()
        
    def delete_profile(self):
        self.delete()

    def __str__(self):
        return str(self.user)
    
    # def __str__(self):
    #     return f"{self.user}, {self.bio}, {self.photo}"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Products(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Pic = models.ImageField(upload_to= "..\images", )
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
    def save_products(self):
        self.save()
    
    def delete_products(self):
        self.delete()
        
    @classmethod
    def get_allproducts(cls):
        products = cls.objects.all()
        return products
    

class Orders(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class Customers(models.Model):
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True, blank=False, null=False)
    Phonenumber = models.CharField(max_length=15,blank=False , null=False)
    location = models.CharField(max_length=200)
    
    def save_customers(self):
        self.save()
    
    def delete_customers(self):
        self.delete()

class Reviews(models.Model):
    
    Comment = models.CharField(max_length=1000)
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
