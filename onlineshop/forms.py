from django import forms
from .models import *
from .views import *
from django.contrib.auth.models import User


class AddReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['Comment', 'rating', 'product', 'customer']  # Include all necessary fields
        widgets = {
            'Comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'product': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for products
            'customer': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for customers
        }