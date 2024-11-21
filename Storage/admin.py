from django.contrib import admin
from Storage.models import *

# Register your models here.
admin.site.register(Chasis)
admin.site.register(Pc)
admin.site.register(Lector)
admin.site.register(Ranura_Expansion)
admin.site.register(Almacenamiento)
admin.site.register(Placa_Base)
admin.site.register(Procesador)
admin.site.register(Ram)
admin.site.register(Tarjeta_Red)
admin.site.register(Fuente)
admin.site.register(Perifericos)
admin.site.register(Incidencias)


#para salgan hay q en el self ponerle un string o aqui sobreescribir y registrar ___Admin 