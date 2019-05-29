import sys
import logging
logging.basicConfig(stream=sys.stderr)
path = '/var/www/html'
if path not in sys.path:
    sys.path.insert(0, path)

from catalog import app as application

