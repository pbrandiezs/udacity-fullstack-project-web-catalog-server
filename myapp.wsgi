import sys
import logging
logging.basicConfig(stream=sys.stderr)
path = '/var/www/html'
if path not in sys.path:
    sys.path.insert(0, path)

app.secret_key = 'super_secret_key'
from catalog import app as application

