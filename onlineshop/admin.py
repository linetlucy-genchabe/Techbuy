from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Orders)
admin.site.register(Customers)
admin.site.register(Brand)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Reviews)

