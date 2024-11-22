import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HardWare.settings')

app = Celery('HardWare')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.result_backend = 'django-db'