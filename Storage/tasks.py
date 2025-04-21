from celery import shared_task
from .utils import *


@shared_task(name='procesar_json_files')
def task_procesar_json_files():
    procesar_json_files()


