from django.urls import  re_path as url, include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'$', views.index, name='index'),
    # admin setup module
    path('setup', views.setup, name='setup'),
    path('products/', views.products, name='products'),
    path('reviews', views.reviews, name='reviews'),
    path('new-review', views.new_review, name='new-review'),

    
    path('add_products/', views.add_products, name='add_products'),
    # Add & view Categories
    path('categories/', views.add_categories, name='categories'),
    
    path('contact_us/', views.contact_us, name='contact_us'),
    path('product/<int:product_id>/', views.single_product, name='product_detail')

    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)