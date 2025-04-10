from django import forms
from .models import *
from .views import *
from django.contrib.auth.models import User



class AddReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['Comment', 'rating', 'product', 'customer']
        widgets = {
            'Comment': forms.Textarea(attrs={
                'class': 'form-control custom-style',
                'rows': 3,
                'placeholder': 'Write your review...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control custom-style',
                'min': 1,
                'max': 5
            }),
            'product': forms.Select(attrs={
                'class': 'form-control custom-style'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-control custom-style'
            }),
        }
