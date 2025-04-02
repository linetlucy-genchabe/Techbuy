from django.shortcuts import get_object_or_404, render,redirect
from django.conf import settings
from .models import *


def index(request):
    
    return render(request, 'index.html')



def products(request):
    
    products = Products.objects.all
    
    return render(request, 'public/products.html', {'products':products})



def contact_us(request):
    
    return render(request, 'public/contact_us.html')
