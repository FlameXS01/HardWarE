from celery import shared_task
from .models import Trys 


@shared_task
def mi_tarea():
    nueva_tarea = Trys(resultado=14)
    nueva_tarea.save()
    # Devolver el objeto como un diccionario
    return {
        'id_trys': nueva_tarea.id_trys,
        'resultado': nueva_tarea.resultado,
        # Agrega otros campos que necesites
    }

