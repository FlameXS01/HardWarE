from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
# Create your models here.

class Chasis(models.Model):
    id_chasis = models.BigAutoField(primary_key=True)
    tipo_chasis = models.CharField(max_length=50)  
    serial_board = models.CharField(max_length=50, null=True)  
    
    @property
    def nombre_equipo_relacionado(self):
        if hasattr(self, 'pc'):  
            return self.pc.nombre_equipo
        return "No asignado a ninguna PC"
    
    
    def __str__(self):
        return self.pc.nombre_equipo  

class Pc(models.Model):
    id_pc = models.BigAutoField(primary_key=True)
    serial_pc = models.CharField(max_length=50, unique=True)
    so = models.CharField(max_length=50)
    nombre_equipo = models.CharField(max_length=50)
    ultimo_reporte = models.DateField()
    id_chasis = models.OneToOneField(Chasis, null=False, blank=False, on_delete=models.CASCADE, related_name='pc')
    id_entidad = models.ForeignKey('Entidad', null=True, blank=True, on_delete=models.CASCADE) 
    
    def delete(self, *args, **kwargs):
        if self.id_chasis:
            self.id_chasis.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.nombre_equipo

class Lector(models.Model):
    id_lector = models.BigAutoField(primary_key=True)
    desc_lector = models.CharField(max_length=150)
    tipo_lector = models.CharField(max_length=150)
    id_chasis = models.OneToOneField(Chasis, null = False, blank = False, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.id_chasis)

class Ranura_Expansion(models.Model):
    id_ranuras_expansion = models.BigAutoField(primary_key=True)
    id_slot = models.CharField(max_length=50) #a chardfield
    #id_board = models.CharField(max_length=50)
    #conector_ranura = models.CharField(max_length=50)
    uso = models.CharField(max_length=50)
    id_chasis = models.ForeignKey(Chasis, null = False, blank = False, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.id_chasis

class Almacenamiento(models.Model):
    id_almacenamiento = models.BigAutoField(primary_key=True)
    no_serie_alm = models.CharField(max_length=100, unique=True)
    tipo_alm = models.CharField(max_length=50)
    interface_alm = models.CharField(max_length=50)
    modelo_alm = models.CharField(max_length=50)
    capacidad_alm = models.BigIntegerField()
    id_chasis = models.ForeignKey(Chasis, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_chasis
    
    @property
    def capacidad_gb(self):
        return round(self.capacidad_alm / 1024, 2)

class Placa_Base(models.Model):
    id_placa = models.BigAutoField(primary_key=True)
    no_serie_placa = models.CharField(max_length=50)
    fabricante_placa = models.CharField(max_length=50)
    modelo_placa = models.CharField(max_length=50)
    id_chasis = models.OneToOneField(Chasis, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.modelo_placa

class Procesador(models.Model):
    id_procesador = models.BigAutoField(primary_key=True)
    desc_procesador = models.CharField(max_length=100)
    velocidad_procesador = models.IntegerField()
    #conector = models.CharField(max_length=50)
    arq_procesador = models.CharField(max_length=50)
    id_placa = models.OneToOneField(Placa_Base, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_placa

class Ram(models.Model):
    id_ram = models.BigAutoField(primary_key=True)
    capacidad_ram = models.IntegerField()
    no_serie_ram = models.CharField(max_length=50)
    tipo_ram = models.CharField(max_length=50)
    id_placa = models.ForeignKey(Placa_Base, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_placa

class Tarjeta_Red(models.Model):
    id_tarjeta = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    ip  = models.CharField(max_length=50)
    subnet = models.CharField(max_length=50)
    gateway = models.CharField(max_length=50)
    id_placa = models.ForeignKey(Placa_Base, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_placa

class Fuente(models.Model):
    id_fuente = models.BigAutoField(primary_key=True) 
    fabricante_fuente = models.CharField(max_length=50) 
    no_serie_fuente = models.CharField(max_length=50)
    potencia_fuente = models.CharField(max_length=50)
    id_chasis = models.OneToOneField(Chasis, null = False, blank = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.id_chasis

class Perifericos(models.Model):
    id_periferico = models.BigAutoField(primary_key=True)
    tipo_periferico = models.CharField(max_length=50)
    no_serie_periferico = models.CharField(max_length=50)
    fabricante_periferico = models.CharField(max_length=50)
    modelo_periferico = models.CharField(max_length=50)
    id_pc = models.ForeignKey(Pc, null=False, blank=False, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.tipo_periferico    

class Incidencias(models.Model):
    id_incidencia = models.BigAutoField(primary_key=True)
    desc_incidencia = models.CharField(max_length=50)
    fecha_incidencia = models.CharField(max_length=50)
    observacion = models.CharField(max_length=250)
    id_pc = models.ForeignKey(Pc, null=False, blank=False, on_delete=models.CASCADE)    

    def __str__(self):
        return self.observacion

class Entidad(models.Model):
    id_entidad = models.BigAutoField(primary_key=True)
    tipoEntidad = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class ExpedienteHistorico(models.Model):
    id_historico = models.BigAutoField(primary_key=True)
    fecha_version = models.DateTimeField(auto_now_add=True)
    datos_json = models.JSONField(encoder=DjangoJSONEncoder)
    pc = models.ForeignKey(Pc, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Versión {self.fecha_version} - {self.pc.nombre_equipo}"

class PendienteActualizacion(models.Model):
    id_pendiente = models.BigAutoField(primary_key=True)
    id_pc = models.ForeignKey(Pc, on_delete=models.CASCADE)
    fecha_pendiente = models.DateTimeField(auto_now_add=True)
    datos_nuevos = models.JSONField()  
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('APLICADO', 'Aplicado'),
        ('RECHAZADO', 'Rechazado')
    ], default='PENDIENTE')