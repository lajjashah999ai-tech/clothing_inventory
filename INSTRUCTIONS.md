# Instructions — Vastradhaga Clothing Shop

## Running the App Locally

### First Time Setup
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run database migrations
python manage.py migrate

# 3. Create admin login
python manage.py createsuperuser
# Enter: username, email (optional), password

# 4. Start the server
python manage.py runserver
```

Open browser: **http://127.0.0.1:8000/**

### Daily Start
```bash
source venv/bin/activate
python manage.py runserver
```

---

## Common Tasks

### Add a New Admin User
```bash
source venv/bin/activate
python manage.py createsuperuser
```

### Reset Admin Password
```bash
source venv/bin/activate
python manage.py changepassword <username>
```

### Backup the Database (SQLite)
```bash
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

### Apply Database Changes (after model edits)
```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

---

## Deploying to Render (Internet)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create Render account** at render.com

3. **New Web Service** → Connect GitHub repo

4. **Set Build Command:**
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```

5. **Set Start Command:**
   ```
   gunicorn vastradhaga.wsgi
   ```

6. **Set Environment Variables on Render:**
   | Key | Value |
   |---|---|
   | `DJANGO_SETTINGS_MODULE` | `vastradhaga.settings.production` |
   | `SECRET_KEY` | (generate a random 50-char string) |
   | `DATABASE_URL` | (from Render PostgreSQL → Internal URL) |
   | `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

7. Also create a **Render PostgreSQL** database and copy the Internal Database URL.

---

## Day-to-Day Usage Guide

### Recording a Sale
1. Click **New Sale** in sidebar
2. Select item from dropdown
3. Enter quantity
4. Click **Add Another Item** to add more
5. Click **Complete Sale**
6. Stock auto-updates

### Adding Inventory
1. Go to **Items** → **Add Item**
2. Fill in all fields
3. Submit

### Restocking an Item
1. Go to **Items**
2. Click edit (pencil icon) on the item
3. Use the **Restock** panel on the right
4. Enter quantity to ADD (not replace)
5. Click **Add Stock**

### Adding a New Category
1. Go to **Categories**
2. Type name in the form on the left
3. Click **Add Category**

### Viewing Reports
- **Stock Report**: Full inventory with values
- **Low Stock**: Items with < 5 units (restock these)
- **Sales Report**: Daily revenue breakdown
