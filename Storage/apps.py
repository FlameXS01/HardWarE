from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError

class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Storage'

    def ready(self):
        # Verificar la conexión a la base de datos
        db_conn = connections['default']
        try:
            db_conn.ensure_connection()
            print("Conexión a la base de datos establecida correctamente.")
        except OperationalError:
            print("No se pudo conectar a la base de datos.")