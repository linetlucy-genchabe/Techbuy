from django.shortcuts import get_object_or_404, render,redirect
from django.conf import settings


def index(request):
    
    return render(request, 'index.html')
