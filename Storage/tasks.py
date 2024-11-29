from celery import shared_task
from .models import Trys 
import os
import socket 


@shared_task
def scan_connected_devices():
    print('hola')
    
    # Procesar y devolver los dispositivos
    return 1
