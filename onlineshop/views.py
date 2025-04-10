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
from django.http import JsonResponse




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
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    return render(request, 'public/products.html', {'categories':categories, 'brands':brands,'products':products})

def reviews(request):
    
    reviews = Reviews.objects.all
    
    return render(request, 'reviews.html', {'reviews':reviews})

def new_review(request):
    
    if request.method == 'POST':
        form = AddReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            
            review.save()
            return redirect('reviews')

    else:
        form = AddReviewsForm()
    return render(request, 'add_review.html', {"form": form})

# @login_required
def add_products(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        pic = request.FILES.get('pic')
        description = request.POST.get('description')
        product_category_id = request.POST.get('category')
        price = request.POST.get('price')
        product_brand_id = request.POST.get('brand')

        category_instance = Category.objects.filter(id=product_category_id).first()
        brand_instance = Brand.objects.filter(id=product_brand_id).first()

        if not category_instance:
            return JsonResponse({'success': False, 'message': 'Invalid Category'})

        if not brand_instance:
            return JsonResponse({'success': False, 'message': 'Invalid Brand'})

        Products.objects.create(
            name=name,
            pic=pic,
            description=description,
            product_category=category_instance,
            product_brand=brand_instance,
            price=price
        )

        return JsonResponse({'success': True, 'message': 'Product Added Successfully'})

    return render(request, 'public/add_products.html', {
        'categories': categories,
        'brands': brands
    })
    
    


def single_product(request, product_id):
    product = Products.objects.get(id=product_id)
    current_user = request.user
    # user = User.objects.get(username=current_user.username)
    return render(request, 'public/product_detail.html', {'product': product,})




def add_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Category.objects.create(name=name, description=description)
            return JsonResponse({'success': True, 'message': 'Category added successfully!'})

        return JsonResponse({'success': False, 'message': 'Name is required.'})

    categories = Category.objects.all()
    return render(request, 'setup/categories.html', {'categories': categories})


# Brands additions
def add_brands(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            return JsonResponse({'success': True, 'message': 'Brand added successfully!'})

        return JsonResponse({'success': False, 'message': 'Name is required.'})

    brands = Brand.objects.all()
    return render(request, 'setup/brands.html', {'brands': brands})




def contact_us(request):
    
    return render(request, 'public/contact_us.html')



def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Products, id=product_id)

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
            }

        request.session['cart'] = cart

        return JsonResponse({
            'success': True,
            'message': f"{product.name} added to cart!",
            'cartItemCount': sum(item['quantity'] for item in cart.values())
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})



def view_cart(request):
    cart = request.session.get('cart', {})
    return JsonResponse({
        'success': True,
        'cart': cart,
        'cartItemCount': sum(item['quantity'] for item in cart.values()),
        'totalPrice': sum(item['price'] * item['quantity'] for item in cart.values())
    })









