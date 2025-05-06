import os
import json
from django.conf import settings
import logging
from .models import *
from django.db import transaction
from datetime import datetime
from HardWare.settings import JSON_INCOMING_DIR


logger = logging.getLogger('Storage')




def procesar_json_files():
    for filename in os.listdir(JSON_INCOMING_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(JSON_INCOMING_DIR, filename)
            try:
                with open(filepath, 'r', encoding='ISO-8859-1') as f:
                    data = json.load(f)
                    procesar_pc( data )
                    # Eliminar el archivo después de procesarlo
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Archivo {filename} >>>>>> procesado y eliminado correctamente <<<<<<")
                else:
                    logger.warning(f"El archivo {filename} no existe o ya fue eliminado")

            except Exception as e:
                logger.error(f"Error procesando {filename}: {str(e)}")
                timestamp = os.path.getmtime(filepath)
                fecha_formateada = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
                nuevo_nombre = f"{fecha_formateada}-{filename}"
                os.rename(filepath, os.path.join(JSON_INCOMING_DIR, 'error', nuevo_nombre))
                
def procesar_pc(data):
    with transaction.atomic():
        pc, created = procesar_pc_base(data)
        if created:
            crear_componentes(pc, data )
        else:
            actualizar_componentes(pc, data )

def procesar_pc_base(data):
    pc_name = data['pc_name']
    #serial_pc = ''
    serial_pc_prov= data['motherboards'][0]['serial'].strip()
    if serial_pc_prov != "Default string" and serial_pc_prov != 'To be filled by O.E.M.':
        serial_pc = serial_pc_prov
    else:
        serial_pc = serial_pc_prov + pc_name
    
    try:
        segmento_medio = pc_name.split('-')[1].strip().upper()
    except IndexError:
        segmento_medio = "DESCONOCIDO"
    
    datos_entidad = obtener_entidad(segmento_medio)
    
    # Crear o obtener la entidad
    entidad, _ = Entidad.objects.get_or_create(
        nombre=datos_entidad['nombre'],
        defaults={'tipoEntidad': datos_entidad['tipo']}
    )   
    
    chasis = procesar_chasis(data, serial_pc)
    
    pc, created = Pc.objects.update_or_create(
        serial_pc=serial_pc,
        defaults={
            'nombre_equipo': data['pc_name'],
            'so': data['operating_systems'][0]['version'],
            'ultimo_reporte': datetime.now().date(),
            'id_chasis':chasis,
            'id_entidad': entidad
        }
    )
    print(pc)
    return pc, created

def procesar_chasis(data, serial_board):
    chasis, created = Chasis.objects.get_or_create(
        serial_board=serial_board,
        defaults={
            'tipo_chasis': data['chassis'][0]['type_name']
        }
    )
    return chasis

def crear_componentes(pc, data):
    # Lógica para crear todos los componentes relacionados
    placa = Placa_Base.objects.create(
        no_serie_placa=data['motherboards'][0]['serial'].strip(),
        fabricante_placa=data['motherboards'][0]['manufacturer'],
        modelo_placa=data['motherboards'][0]['product'].strip(),
        id_chasis=pc.id_chasis
    )
    
    # Procesador
    cpu = data['cpus'][0]
    operating_systems = data['operating_systems'][0]
    Procesador.objects.create(
        desc_procesador=cpu['name'],
        velocidad_procesador=cpu['clock'],
        arq_procesador=operating_systems['architecture'],
        id_placa=placa
    )
    
    # RAM
    for mem in data['memory']:
        Ram.objects.create(
            capacidad_ram=mem['capacity_gb'],
            no_serie_ram=mem['serial'],
            tipo_ram=f"DDR{mem['type_code']}",
            id_placa=placa
        )
    
    # Tarjetas de Red
    for adapter in data['network_adapters']:
        if adapter['ip'] != 'N/A':
            Tarjeta_Red.objects.create(
                mac=adapter['mac'],
                ip=adapter['ip'],
                subnet=adapter['subnet'],
                gateway=adapter['gateway'],
                id_placa=placa
            )
    
    
    # Almacenamiento
    for hdd in data['hard_drives']:
        Almacenamiento.objects.create(
            no_serie_alm=hdd['serial'],
            tipo_alm=hdd['interface'],
            interface_alm=hdd['model'],
            modelo_alm=hdd['model'],
            capacidad_alm=hdd['size_gb'] * 1024,  # Convertir GB a MB
            id_chasis=pc.id_chasis
        )

def actualizar_componentes(pc, data):
    cambios = detectar_cambios(pc, data)
    
    if cambios:
        registrar_incidencia(pc, cambios)
        
    else:
        pc.ultimo_reporte = datetime.now().date()
        pc.save()

def detectar_cambios(pc, new_data):
    cambios = {}
    
    # Comparar datos básicos
    old_data = {
        'nombre_equipo': pc.nombre_equipo,
        'so': pc.so,
        'chasis': pc.id_chasis.tipo_chasis
    }
    
    new_values = {
        'nombre_equipo': new_data['pc_name'],
        'so': new_data['operating_systems'][0]['version'],
        'chasis': new_data['chassis'][0]['type_name']
    }
    
    for campo, valor_viejo in old_data.items():
        if valor_viejo != new_values[campo]:
            cambios[campo] = f"{valor_viejo} -> {new_values[campo]}"
    
    # Comparar componentes hardware (implementar lógica similar para cada modelo)
    # Ejemplo para RAM:
    rams_viejas = Ram.objects.filter(id_placa__id_chasis=pc.id_chasis)
    for i, ram_nueva in enumerate(new_data['memory']):
        if i < len(rams_viejas):
            ram_vieja = rams_viejas[i]
            if ram_vieja.no_serie_ram != ram_nueva['serial']:
                cambios[f'RAM_{i}'] = f"Serial cambió {ram_vieja.no_serie_ram} -> {ram_nueva['serial']}"
    
    return cambios

def registrar_incidencia(pc, cambios):
    desc = "Cambios detectados:\n" + "\n".join([f"{k}: {v}" for k, v in cambios.items()])
    
    Incidencias.objects.create(
        desc_incidencia="Modificación de hardware",
        fecha_incidencia=datetime.now().date(),
        observacion=desc[:50], 
        id_pc=pc
    )

def obtener_entidad(segmento):
    # Buscar en el diccionario
    entrada = MAPEO_ENTIDADES.get(segmento, None)
    
    if entrada:
        return {'nombre': entrada[0], 'tipo': entrada[1]}
    else:
        return {'nombre': segmento, 'tipo': 'Otros'}
        

MAPEO_ENTIDADES = {
    # Complejos
    'SSP': ('Complejo Sancti Spiritus', 'Complejo '),
    'CAB': ('Complejo Cabaiguan', 'Complejo'),
    'TAG': ('Complejo Taguasco', 'Complejo'),
    'TRI': ('Complejo Trinidad', 'Complejo'),
    
    # UEBs
    'REG': ('Almacén Distribuidor', 'UEB'),
    
    'CEL': ('Centro de Elaboración', 'UEB'),
    
    'SST': ('División Tecnológica', 'UEB'),
    
    'FX':  ('Fincimex', 'UEB'),
    
    'ADM': ('Sucursal', 'UEB'),
    'COM': ('Sucursal', 'UEB'),
    'ECO': ('Sucursal', 'UEB'),
    'GER': ('Sucursal', 'UEB'),
    'INF': ('Sucursal', 'UEB'),
    'PRO': ('Sucursal', 'UEB'),
    'RH':  ('Sucursal', 'UEB'),
    
    'VIR': ('Tiendas Virtuales', 'UEB'),
    
    'MAY': ('Mayorista', 'UEB'),
    
    'ECU': ('Logística', 'UEB'),
    'INV': ('Logística', 'UEB'),
    'MTTO':('Logística', 'UEB'),
    'TRA': ('Logística', 'UEB')
}