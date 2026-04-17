from django import forms
from .models import Category, Item


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'size', 'quantity', 'purchase_price', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. S, M, L, XL, 32, Free Size'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }
        labels = {
            'purchase_price': 'Purchase Price (₹)',
            'selling_price': 'Selling Price (₹)',
        }


class RestockForm(forms.Form):
    restock_qty = forms.IntegerField(
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Add stock quantity', 'min': '1'}),
        label='Add Stock Quantity'
    )
