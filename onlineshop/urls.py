from django.urls import  re_path as url, include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'$', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('contact_us/', views.contact_us, name='contact_us')

    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)