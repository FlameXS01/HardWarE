from celery import shared_task
from .import_data import import_data  

@shared_task
def run_import_data():
    import_data()
    
