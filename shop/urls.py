from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Products (items)
    path('products/', views.item_list, name='item_list'),
    path('products/add/', views.item_add, name='item_add'),
    path('products/bulk-add/', views.item_bulk_add, name='item_bulk_add'),
    path('products/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('products/<int:pk>/delete/', views.item_delete, name='item_delete'),

    # Sales / POS
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/new/', views.pos_view, name='pos'),
    path('sales/<int:pk>/invoice/', views.invoice_view, name='invoice'),

    # Reports
    path('reports/stock/', views.report_stock, name='report_stock'),
    path('reports/stock/export/', views.report_stock_csv, name='report_stock_csv'),
    path('reports/low-stock/', views.report_low_stock, name='report_low_stock'),
    path('reports/sales/', views.report_sales, name='report_sales'),
    path('reports/sales/export/', views.report_sales_csv, name='report_sales_csv'),
]
