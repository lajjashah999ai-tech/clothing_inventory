# shop/ — Django App

## Models (shop/models.py)
- **Category**: name (unique), created_at
- **Item**: name, category (FK), size, quantity, purchase_price, selling_price, is_active
- **Sale**: sale_date, total_amount, notes
- **SaleItem**: sale (FK), item (FK), quantity, unit_price (snapshot), subtotal

## Views (shop/views.py)
All views are function-based, protected with `@login_required`.

| View | URL | Purpose |
|---|---|---|
| `login_view` | /login/ | Auth |
| `dashboard_view` | / | Stats overview |
| `category_list` | /categories/ | List + inline add |
| `category_edit` | /categories/<pk>/edit/ | Edit |
| `category_delete` | /categories/<pk>/delete/ | Delete |
| `item_list` | /items/ | List with search |
| `item_add` | /items/add/ | Add item |
| `item_edit` | /items/<pk>/edit/ | Edit + restock |
| `item_delete` | /items/<pk>/delete/ | Soft delete |
| `pos_view` | /sales/new/ | POS entry |
| `sale_list` | /sales/ | History |
| `report_stock` | /reports/stock/ | Stock table |
| `report_low_stock` | /reports/low-stock/ | Items qty < 5 |
| `report_sales` | /reports/sales/ | Daily summary |

## Templates (shop/templates/shop/)
- `base.html` — Sidebar layout, Bootstrap 5, flash messages
- `login.html` — Login card
- `dashboard.html` — 4 stat cards + low stock table
- `categories.html` — Inline add + list
- `items/list.html` — Searchable table
- `items/add.html` / `edit.html` — Forms
- `sales/pos.html` — Dynamic POS form with JS
- `sales/list.html` — History log
- `reports/stock.html` / `low_stock.html` / `sales.html` — Reports

## Business Rules
- Low stock threshold: quantity < 5
- POS sale: validates stock before saving, uses `transaction.atomic()`
- Item delete: soft delete only (sets `is_active=False`)
- Category delete: blocked if items exist under it
