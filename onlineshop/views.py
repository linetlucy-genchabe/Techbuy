from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import sweetify



def index(request):
    products = Products.objects.all
    
    return render(request, 'index.html', {'products':products})

def setup(request):
    product_count = Products.objects.count()
    category_count = Category.objects.count()
    brand_count = Brand.objects.count()
    
    return render(request, 'setup/setup.html', {'product_count':product_count, 'category_count':category_count,'brand_count':brand_count })



def products(request):
    
    products = Products.objects.all
    
    return render(request, 'public/products.html', {'products':products})

def reviews(request):
    
    reviews = Reviews.objects.all
    
    return render(request, 'reviews.html', {'reviews':reviews})

def new_review(request):
    
    if request.method == 'POST':
        form = AddReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            
            review.save()
            return redirect('index')

    else:
        form = AddReviewsForm()
    return render(request, 'add_review.html', {"form": form})

# @login_required
def add_products(request):
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        # Check if vendor exists
        
            name = request.POST.get('name')
            pic = request.FILES.get('pic')
            description = request.POST.get('description')
            product_category_id = request.POST.get('category')
            price = request.POST.get('price')
            product_brand_id = request.POST.get('brand')
            # stock = request.POST.get('brand')
        
            # Ensure category exists
            category_instance = Category.objects.filter(id=product_category_id).first()
            print("category is:", category_instance)
            product_instance = Brand.objects.filter(id=product_brand_id).first()


            if category_instance:
                products = Products(
                    
                    pic=pic,
                    description=description,
                    name=name,
                    product_category=category_instance,
                    product_brand=product_instance,
                    price=price,
                    
                )

                products.save()
                sweetify.success(request, 'Success!', text='Product Added Successfully', persistent='Ok')

                return redirect('products')

            else:
                print("⚠️ Invalid Category:", product_category_id)
    
    return render(request, 'public/add_products.html', {'categories':categories, 'brands':brands})



def single_product(request, product_id):
    product = Products.objects.get(id=product_id)
    current_user = request.user
    # user = User.objects.get(username=current_user.username)
    return render(request, 'public/product_detail.html', {'product': product,})

def add_categories(request):
    category = None
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        # if name:
            # Category.objects.create(name=name)
        category = Category(name=name,description=description)
        category.save()
        return redirect('categories') 
    categories = Category.objects.all()
    
    return render(request, 'setup/categories.html', {'category':category,'categories':categories})


def contact_us(request):
    
    return render(request, 'public/contact_us.html')
