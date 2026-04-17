import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vastradhaga.settings.production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel expects the WSGI app to be named 'app'
app = application
