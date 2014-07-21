from gevent import monkey
monkey.patch_all()
import pkgutil
import os

os.environ['GEVENT_RESOLVER'] = 'ares'
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
