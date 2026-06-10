from django import forms
from django.core.exceptions import ValidationError
from shop.models import Category, Product, Ad


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Category name cannot be empty')
        if len(name) > 50:
            raise ValidationError('Category name must be 50 characters or less')
        return name


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'contact_phone', 'category', 'currency', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Product description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'step': '0.01'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact phone (8 digits)',
                'maxlength': '8'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and float(price) <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Product name cannot be empty')
        if len(name) > 50:
            raise ValidationError('Product name must be 50 characters or less')
        return name


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['name', 'order', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ad name'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Ad name cannot be empty')
        if len(name) > 50:
            raise ValidationError('Ad name must be 50 characters or less')
        return name

    def clean_order(self):
        order = self.cleaned_data.get('order')
        if order is not None and order < 0:
            raise ValidationError('Order must be a non-negative integer')
        return order
