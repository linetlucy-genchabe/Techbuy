from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth import authenticate, logout,login as auth_login 
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from django.http import JsonResponse
from django.contrib.auth.models import User  
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.sessions.models import Session



def index(request):
    products = Products.objects.all
    reviews = Reviews.objects.all
    
    return render(request, 'index.html', {'products':products, 'reviews':reviews},)


# Authentication Views
# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            
            sweetify.toast(request, 'Passwords do not match!', icon='error', position='top-end', timer=3000)
            return redirect('register')

        if User.objects.filter(username=username).exists():
            sweetify.toast(request, 'Username already taken!', icon='error', position='top-end', timer=3000)
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
        sweetify.toast(request, 'Registartion succesful. Kindly Login!', icon='success', position='top-end', timer=3000)
        return redirect('login')
    return render(request, 'authentication/register.html')


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user) 
            
            # Set customer_id in session, assuming user has related customer
            try:
                request.session['customer_id'] = user.customer.id
            except AttributeError:
                # Handle if user has no related customer object
                request.session['customer_id'] = None

            sweetify.toast(request, f'Welcome back, {user.username}!', icon='success', position='top-end', timer=3000)
            return redirect('index')  
        else:
            sweetify.toast(request, 'Invalid username or password.', icon='error', position='top-end', timer=3000)
            return redirect('login')  

    return render(request, 'authentication/login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('index');

# check admin Role to use when allowing only admin users to access administrative views

def is_admin(user):
    return (
        user.is_authenticated and 
        hasattr(user, 'profile') and  
        user.profile.role == 'admin'  
    )
    
# utility function to enable throwing of forbidden error if user is not admin
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def setup(request):
    product_count = Products.objects.count()
    category_count = Category.objects.count()
    brand_count = Brand.objects.count()
    
    return render(request, 'setup/setup.html', {'product_count':product_count, 'category_count':category_count,'brand_count':brand_count })


@login_required
@admin_required
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

@login_required
@admin_required
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
    return render(request, 'public/product_detail.html', {'product': product,})



@login_required
@admin_required
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
@login_required
@admin_required
def add_brands(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            return JsonResponse({'success': True, 'message': 'Brand added successfully!'})

        return JsonResponse({'success': False, 'message': 'Name is required.'})

    brands = Brand.objects.all()
    return render(request, 'setup/brands.html', {'brands': brands})

# to render Permission Denied Error.
def permission_denied_view(request, exception=None):
    return render(request, 'public/403.html', status=403)

def contact_us(request):
    
    return render(request, 'public/contact_us.html')



# def add_to_cart(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = int(request.POST.get('quantity', 1))

#         product = get_object_or_404(Products, id=product_id)

#         cart = request.session.get('cart', {})

#         if product_id in cart:
#             cart[product_id]['quantity'] += quantity
#         else:
#             cart[product_id] = {
#                 'name': product.name,
#                 'price': float(product.price),
#                 'quantity': quantity,
#             }

#         request.session['cart'] = cart

#         return JsonResponse({
#             'success': True,
#             'message': f"{product.name} added to cart!",
#             'cartItemCount': sum(item['quantity'] for item in cart.values())
#         })

#     return JsonResponse({'success': False, 'message': 'Invalid request'})
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Products.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.save()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

        # Clean old items
        # cart.delete_old_items()

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:

            cart[product_id] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'product_id': product.id,
            }

        request.session['cart'] = cart
            item.quantity = quantity
        item.save()


        return JsonResponse({
            'success': True,
            'message': f"{product.name} added to cart!",
            'cartItemCount': cart.items.count(),
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})




def view_cart(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
        request.session.modified = True

    cart = request.session.get('cart', {})
    return JsonResponse({
        'success': True,
        'cart': cart,
        'cartItemCount': sum(item['quantity'] for item in cart.values()),
        'totalPrice': sum(item['price'] * item['quantity'] for item in cart.values())
    })




def order_summary(request):
    cart = request.session.get('cart', {})

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    cart_items = [{
        'name': item.get('name'),
        'quantity': item.get('quantity'),
        'price': item.get('price'),
        'product_id': item.get('product_id'),  # Use .get() to avoid KeyError
        'total': item.get('price') * item.get('quantity') if item.get('price') and item.get('quantity') else 0
    } for item in cart.values()]

    return render(request, 'public/order.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def checkout_order(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        count = int(request.POST.get('count', 0))
        if count == 0:
            return HttpResponseBadRequest("Missing data.")

        for i in range(1, count + 1):
            product_id = request.POST.get(f'product_id_{i}')
            customer_id = request.POST.get(f'customer_id_{i}')
            quantity = request.POST.get(f'quantity_{i}')

            print(f"product_id={product_id}, customer_id={customer_id}, quantity={quantity}")

            if not all([product_id, customer_id, quantity]):
                return HttpResponseBadRequest("Missing data in item {}".format(i))

            try:
                product = Products.objects.get(id=int(product_id))
                customer = Customers.objects.get(id=int(customer_id))
                quantity = int(quantity)
            except (Products.DoesNotExist, Customers.DoesNotExist, ValueError):
                return HttpResponseBadRequest("Invalid product or customer for item {}".format(i))

            total = product.price * quantity

            # Save order
            Orders.objects.create(
                product=product,
                customer=customer,
                quantity=quantity,
                Totalprice=total,
            )

            # Optional: Save to cart model
            Cart.objects.create(
                product=product,
                customer=customer,
                quantity=quantity,
                price=product.price,
            )

        # Optionally clear the cart
        request.session['cart'] = {}

        return redirect('product_detail')  
   
@login_required
@admin_required
def view_ordered_items(request):
    orders = Orders.objects.select_related('product', 'customer')
    return render(request, 'public/ordered_items.html', {'orders': orders})


