# Vastradhaga Clothing Shop — Project Overview

## What This Is
A custom-built inventory management + POS web application for Vastradhaga Clothing Shop.
Built with Django 4.2, Bootstrap 5, SQLite (local) / PostgreSQL (cloud).

## Tech Stack
- **Backend**: Python 3.x + Django 4.2
- **Database**: SQLite (local dev), PostgreSQL (Render/cloud)
- **Frontend**: Django Templates + Bootstrap 5 (CDN)
- **Static files**: WhiteNoise
- **Deployment**: Gunicorn + Render.com

## Project Structure
```
clothing_inventory/
├── manage.py               # Entry point
├── requirements.txt        # Python dependencies
├── Procfile                # Render/Heroku deployment
├── .env                    # Local env vars (not committed)
├── vastradhaga/            # Django project config
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── local.py        # Local dev (SQLite)
│   │   └── production.py   # Production (PostgreSQL)
│   └── urls.py             # Root URL config
└── shop/                   # Main Django app
    ├── models.py            # Category, Item, Sale, SaleItem
    ├── views.py             # All views
    ├── urls.py              # URL patterns
    ├── forms.py             # Django forms
    └── templates/shop/     # All HTML templates
```

## How to Run Locally
```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open: http://127.0.0.1:8000/

## Key Conventions
- All views are function-based with `@login_required`
- Settings split: `local.py` for dev, `production.py` for cloud
- Soft delete on items (`is_active=False`), hard delete on categories
- Stock transactions use `transaction.atomic()` to prevent partial state
- Price snapshots stored in `SaleItem.unit_price` at time of sale
