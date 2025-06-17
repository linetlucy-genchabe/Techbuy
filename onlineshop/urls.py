from django.urls import  re_path as url, include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler403



handler403 = 'onlineshop.views.permission_denied_view'
urlpatterns = [
    url(r'$', views.index, name='index'),
    
    # Authentication
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # admin setup module
    path('setup', views.setup, name='setup'),
    path('products/', views.products, name='products'),
    path('reviews', views.reviews, name='reviews'),
    path('new-review', views.new_review, name='new-review'),

    
    path('add_products/', views.add_products, name='add_products'),
    # Add & view Categories
    path('categories/', views.add_categories, name='categories'),
    # Add Brands
    path('brands/', views.add_brands, name='brands'),
    
    path('contact_us/', views.contact_us, name='contact_us'),
    path('product/<int:product_id>/', views.single_product, name='product_detail'),
    
    # Add to Cart
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    # view cart
    # path('view-cart/', views.view_cart, name='view_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    # UPDATE CART
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    
    # UPDATE DISCOUNT ON PRODUCTS
    
    path('manage-discount/<int:product_id>/', views.manage_discount, name='manage_discount'),

    
     # odder now
    path('order/', views.order_summary, name='order'),


    path('checkout/', views.checkout_order, name='checkout_order'),
    path('view-ordered-items/', views.view_ordered_items, name='view_ordered_items'),
    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)