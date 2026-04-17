from django.contrib import admin
from .models import Category, Item, Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'size', 'quantity', 'selling_price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sale_date', 'total_amount']
    inlines = [SaleItemInline]
