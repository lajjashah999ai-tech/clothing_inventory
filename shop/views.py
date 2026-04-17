import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import Category, Item, Sale, SaleItem
from .forms import CategoryForm, ItemForm, RestockForm


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    today = timezone.localdate()

    # Core stats
    total_items = Item.objects.filter(is_active=True).count()
    total_stock = Item.objects.filter(is_active=True).aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_items = Item.objects.filter(is_active=True, quantity__lt=5).select_related('category').order_by('quantity')
    today_sales = Sale.objects.filter(sale_date__date=today).aggregate(
        count=Count('id'), revenue=Sum('total_amount')
    )

    # Inventory value (qty × selling_price)
    inv_val_rows = Item.objects.filter(is_active=True).values_list('quantity', 'selling_price')
    inventory_value = sum(q * p for q, p in inv_val_rows)

    # Category tiles
    categories = Category.objects.annotate(
        item_count=Count('items', filter=Q(items__is_active=True)),
        total_stock=Sum('items__quantity', filter=Q(items__is_active=True))
    )

    # Category → Product tree (tabbed)
    all_cats = Category.objects.prefetch_related('items').all()
    category_tree = []
    for cat in all_cats:
        products = list(cat.items.filter(is_active=True))
        if products:
            category_tree.append({'name': cat.name, 'pk': cat.pk, 'products': products})

    # Top 5 selling products (all time)
    top_sellers = (
        SaleItem.objects
        .values('item__name', 'item__size')
        .annotate(total_sold=Sum('quantity'), revenue=Sum('subtotal'))
        .order_by('-total_sold')[:5]
    )

    # Recent 8 sales for dashboard table
    recent_sales = Sale.objects.prefetch_related('items__item').order_by('-sale_date')[:8]

    # Chart: last 14 days
    chart_data = {}
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        chart_data[d.strftime('%d %b')] = 0
    sales_14d = (
        Sale.objects.filter(sale_date__date__gte=today - timedelta(days=13))
        .annotate(day=TruncDate('sale_date'))
        .values('day')
        .annotate(rev=Sum('total_amount'))
    )
    for row in sales_14d:
        key = row['day'].strftime('%d %b')
        if key in chart_data:
            chart_data[key] = float(row['rev'] or 0)

    context = {
        'total_items': total_items,
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'low_stock_count': low_stock_items.count(),
        'today_sale_count': today_sales['count'] or 0,
        'today_revenue': today_sales['revenue'] or Decimal('0.00'),
        'inventory_value': inventory_value,
        'categories': categories,
        'category_tree': category_tree,
        'top_sellers': top_sellers,
        'recent_sales': recent_sales,
        'chart_labels': list(chart_data.keys()),
        'chart_values': list(chart_data.values()),
    }
    return render(request, 'shop/dashboard.html', context)


# ── Categories ────────────────────────────────────────────────────────────────

@login_required
def category_list(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{form.cleaned_data["name"]}" added.')
            return redirect('category_list')
    categories = Category.objects.annotate(
        item_count=Count('items', filter=Q(items__is_active=True)),
        total_stock=Sum('items__quantity', filter=Q(items__is_active=True))
    ).order_by('name')
    return render(request, 'shop/categories.html', {'form': form, 'categories': categories})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('category_list')
    return render(request, 'shop/category_edit.html', {'form': form, 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f'Category "{category.name}" deleted.')
        except Exception:
            messages.error(request, f'Cannot delete — products exist under "{category.name}".')
    return redirect('category_list')


# ── Products (Items) ──────────────────────────────────────────────────────────

@login_required
def item_bulk_add(request):
    categories = Category.objects.all()
    results = []
    if request.method == 'POST':
        names = request.POST.getlist('name[]')
        cat_ids = request.POST.getlist('category[]')
        sizes = request.POST.getlist('size[]')
        quantities = request.POST.getlist('quantity[]')
        purchase_prices = request.POST.getlist('purchase_price[]')
        selling_prices = request.POST.getlist('selling_price[]')
        saved = 0
        for i, (name, cat_id, size, qty, cost, sell) in enumerate(
            zip(names, cat_ids, sizes, quantities, purchase_prices, selling_prices), start=1
        ):
            name = name.strip()
            if not name:
                continue
            try:
                if not cat_id:
                    results.append({'row': i, 'success': False, 'text': f'"{name}" — category required'})
                    continue
                Item.objects.create(
                    name=name,
                    category_id=int(cat_id),
                    size=size.strip() or 'Free Size',
                    quantity=int(qty or 0),
                    purchase_price=Decimal(cost or '0'),
                    selling_price=Decimal(sell or '0'),
                )
                results.append({'row': i, 'success': True, 'text': f'"{name}" ({size}) added successfully'})
                saved += 1
            except Exception as e:
                results.append({'row': i, 'success': False, 'text': f'"{name}" — {e}'})
        if saved:
            messages.success(request, f'{saved} product{"s" if saved > 1 else ""} added successfully.')
    return render(request, 'shop/items/bulk_add.html', {
        'categories': categories,
        'row_range': range(8),
        'results': results,
    })


@login_required
def item_list(request):
    items = Item.objects.filter(is_active=True).select_related('category')
    q = request.GET.get('q', '').strip()
    cat_filter = request.GET.get('category', '')
    if q:
        items = items.filter(name__icontains=q)
    if cat_filter:
        items = items.filter(category_id=cat_filter)
    categories = Category.objects.all()
    return render(request, 'shop/items/list.html', {
        'items': items, 'categories': categories, 'q': q, 'cat_filter': cat_filter,
    })


@login_required
def item_add(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{form.cleaned_data["name"]}" added.')
            next_url = request.POST.get('next', request.GET.get('next', ''))
            return redirect(next_url or 'item_list')
    categories = Category.objects.all()
    return render(request, 'shop/items/add.html', {'form': form, 'categories': categories})


@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    form = ItemForm(instance=item)
    restock_form = RestockForm()
    if request.method == 'POST':
        if 'restock' in request.POST:
            restock_form = RestockForm(request.POST)
            if restock_form.is_valid():
                qty = restock_form.cleaned_data.get('restock_qty')
                if qty:
                    item.quantity += qty
                    item.save(update_fields=['quantity'])
                    messages.success(request, f'+{qty} units added to "{item.name}". New stock: {item.quantity}.')
                    return redirect('item_list')
        else:
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, f'"{item.name}" updated.')
                return redirect('item_list')
    return render(request, 'shop/items/edit.html', {
        'form': form, 'restock_form': restock_form, 'item': item,
    })


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.is_active = False
        item.save(update_fields=['is_active'])
        messages.success(request, f'"{item.name}" removed from inventory.')
    return redirect('item_list')


# ── POS / Sales ───────────────────────────────────────────────────────────────

@login_required
def pos_view(request):
    items = Item.objects.filter(is_active=True, quantity__gt=0).select_related('category').order_by('name')
    categories = Category.objects.all()

    if request.method == 'POST':
        item_ids = request.POST.getlist('item_id[]')
        quantities = request.POST.getlist('qty[]')
        notes = request.POST.get('notes', '')

        if not item_ids:
            messages.error(request, 'Cart is empty. Add products before completing the sale.')
            return render(request, 'shop/sales/pos.html', {'items': items, 'categories': categories})

        sale_items_data = []
        errors = []
        total = Decimal('0.00')

        for item_id, qty_str in zip(item_ids, quantities):
            if not item_id or not qty_str:
                continue
            try:
                qty = int(qty_str)
                if qty <= 0:
                    continue
                item = Item.objects.get(pk=item_id, is_active=True)
                if item.quantity < qty:
                    errors.append(f'"{item.name}" only has {item.quantity} unit(s) in stock.')
                else:
                    subtotal = item.selling_price * qty
                    total += subtotal
                    sale_items_data.append({'item': item, 'qty': qty, 'subtotal': subtotal})
            except (Item.DoesNotExist, ValueError):
                errors.append('Invalid product or quantity.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'shop/sales/pos.html', {'items': items, 'categories': categories})

        with transaction.atomic():
            sale = Sale.objects.create(total_amount=total, notes=notes)
            for entry in sale_items_data:
                SaleItem.objects.create(
                    sale=sale,
                    item=entry['item'],
                    quantity=entry['qty'],
                    unit_price=entry['item'].selling_price,
                    subtotal=entry['subtotal'],
                )
                entry['item'].quantity -= entry['qty']
                entry['item'].save(update_fields=['quantity'])

        messages.success(request, f'Sale #{sale.pk} recorded — ₹{total}. Invoice ready.')
        from django.urls import reverse
        return redirect(reverse('invoice', kwargs={'pk': sale.pk}) + '?print=1')

    return render(request, 'shop/sales/pos.html', {'items': items, 'categories': categories})


@login_required
def sale_list(request):
    sales = Sale.objects.prefetch_related('items__item').order_by('-sale_date')
    return render(request, 'shop/sales/list.html', {'sales': sales})


@login_required
def invoice_view(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'shop/sales/invoice.html', {'sale': sale})


# ── Reports ───────────────────────────────────────────────────────────────────

@login_required
def report_stock(request):
    items = Item.objects.filter(is_active=True).select_related('category').order_by('category__name', 'name')
    q = request.GET.get('q', '').strip()
    cat_filter = request.GET.get('category', '')
    if q:
        items = items.filter(name__icontains=q)
    if cat_filter:
        items = items.filter(category_id=cat_filter)
    categories = Category.objects.all()
    total_stock = items.aggregate(total=Sum('quantity'))['total'] or 0

    chart_cats = Category.objects.annotate(
        total_stock=Sum('items__quantity', filter=Q(items__is_active=True))
    ).filter(total_stock__gt=0)

    return render(request, 'shop/reports/stock.html', {
        'items': items, 'categories': categories,
        'q': q, 'cat_filter': cat_filter, 'total_stock': total_stock,
        'chart_cats': chart_cats,
    })


@login_required
def report_stock_csv(request):
    items = Item.objects.filter(is_active=True).select_related('category').order_by('category__name', 'name')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Category', 'Size', 'Stock', 'Cost Price', 'Sell Price'])
    for item in items:
        writer.writerow([item.name, item.category.name, item.size, item.quantity, item.purchase_price, item.selling_price])
    return response


@login_required
def report_low_stock(request):
    items = Item.objects.filter(is_active=True, quantity__lt=5).select_related('category').order_by('quantity')
    return render(request, 'shop/reports/low_stock.html', {'items': items})


@login_required
def report_sales(request):
    daily = (
        Sale.objects
        .annotate(date=TruncDate('sale_date'))
        .values('date')
        .annotate(count=Count('id'), revenue=Sum('total_amount'))
        .order_by('-date')
    )
    grand = Sale.objects.aggregate(total_count=Count('id'), total_revenue=Sum('total_amount'))
    total_count = grand['total_count'] or 0
    total_revenue = grand['total_revenue'] or Decimal('0.00')
    avg_sale = round(total_revenue / total_count, 2) if total_count else Decimal('0.00')

    return render(request, 'shop/reports/sales.html', {
        'daily': daily,
        'total_count': total_count,
        'total_revenue': total_revenue,
        'avg_sale': avg_sale,
    })


@login_required
def report_sales_csv(request):
    daily = (
        Sale.objects
        .annotate(date=TruncDate('sale_date'))
        .values('date')
        .annotate(count=Count('id'), revenue=Sum('total_amount'))
        .order_by('-date')
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'No. of Sales', 'Revenue (₹)'])
    for row in daily:
        writer.writerow([row['date'], row['count'], row['revenue']])
    return response
