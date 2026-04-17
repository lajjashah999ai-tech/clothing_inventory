# vastradhaga/ — Django Project Config

## Settings Split
Three settings files under `vastradhaga/settings/`:

| File | Use When | Database |
|---|---|---|
| `local.py` | Running on your PC | SQLite (db.sqlite3) |
| `production.py` | Deployed on Render/cloud | PostgreSQL via DATABASE_URL |

`base.py` contains all shared settings (apps, middleware, templates, static).

## Environment Variables (.env)
| Variable | Required | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | Yes | `vastradhaga.settings.local` or `.production` |
| `SECRET_KEY` | Yes | Django secret key |
| `DATABASE_URL` | Production only | PostgreSQL connection string |
| `ALLOWED_HOSTS` | Production only | Comma-separated allowed hostnames |
| `DEBUG` | Optional | `True` or `False` |

## URLs (vastradhaga/urls.py)
- `/admin/` → Django admin (fallback)
- All other routes → `shop/urls.py`
