import sys
from modulos import config

sys.path.insert(0, config.APP_CONFIG['ruta'])
from holoeasy import app as application
