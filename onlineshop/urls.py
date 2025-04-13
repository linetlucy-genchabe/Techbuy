from django.urls import  re_path as url, include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'$', views.index, name='index'),
    
    # Authentication
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
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
    path('view-cart/', views.view_cart, name='view_cart'),


    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)