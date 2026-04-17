import os
import dj_database_url
from .base import *

DEBUG = False

# Accept Vercel domains, Render, and any custom ALLOWED_HOSTS from env
_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()] + [
    '.vercel.app',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

# CSRF trusted origins for Vercel/Render
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.onrender.com',
]
_custom = os.environ.get('ALLOWED_HOSTS', '')
if _custom:
    for h in _custom.split(','):
        h = h.strip()
        if h:
            CSRF_TRUSTED_ORIGINS.append(f'https://{h}')

# Database — requires DATABASE_URL env var (Neon / Supabase / Render Postgres)
# conn_max_age=0 is required for Vercel serverless (new connection per request)
_db_url = os.environ.get('DATABASE_URL')
if _db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=_db_url,
            conn_max_age=0,          # MUST be 0 for Vercel serverless
            ssl_require=True,
        )
    }
else:
    # Fallback: SQLite (only works on Render/Railway, NOT Vercel)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files — WhiteNoise serves them directly from the WSGI app
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
