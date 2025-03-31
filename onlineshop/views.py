from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    
    return render(request, 'index.html')



def products(request):
    
    products = Products.objects.all
    
    return render(request, 'public/products.html', {'products':products})

# @login_required
def add_products(request):
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        # Check if vendor exists
        
            name = request.POST.get('name')
            pic = request.FILES.get('pic')
            description = request.POST.get('description')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            product_brand = request.POST.get('brand')
            stock = request.POST.get('brand')
        
            # Ensure category exists
            category_instance = Category.objects.filter(id=category_id).first()
            product_instance = Brand.objects.filter(id=product_brand).first()

            if category_instance:
                products = Category(
                    
                    pic=pic,
                    description=description,
                    name=name,
                    category=category_instance,
                    product_brand=product_instance,
                    price=price,
                    
                )

                products.save()

                return redirect('products')

            else:
                print("⚠️ Invalid Category:", category_id)
    
    return render(request, 'public/add_products.html', {'categories':categories, 'brands':brands})







def contact_us(request):
    
    return render(request, 'public/contact_us.html')
