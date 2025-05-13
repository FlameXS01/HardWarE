import os
import json
import logging
from .models import *
from django.db import transaction
from django.forms import model_to_dict
from datetime import datetime
from HardWare.settings import JSON_INCOMING_DIR
from datetime import datetime, date

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

def convertir_fechas(obj):
    """Función recursiva para convertir fechas a strings ISO"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convertir_fechas(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_fechas(element) for element in obj]
    return obj

def crear_snapshot_historico(pc):
    try:
        # Obtener datos base con model_to_dict
        datos_base = {
            'pc': model_to_dict(pc),
            'chasis': model_to_dict(pc.id_chasis)
        }
        
        # Obtener componentes con manejo de relaciones opcionales
        componentes = {}
        
        # Placa Base
        try:
            placa = Placa_Base.objects.get(id_chasis=pc.id_chasis)
            componentes['placa_base'] = model_to_dict(placa)
        except Placa_Base.DoesNotExist:
            componentes['placa_base'] = None
        
        # Procesador
        try:
            componentes['procesador'] = model_to_dict(Procesador.objects.get(id_placa=placa)) if placa else None
        except Procesador.DoesNotExist:
            componentes['procesador'] = None
        
        # Tarjeta de Red (usamos filter en lugar de get para relaciones 1-N)
        componentes['tarjetas_red'] = list(Tarjeta_Red.objects.filter(id_placa=placa).values()) if placa else []
        
        # RAM
        componentes['rams'] = list(Ram.objects.filter(id_placa=placa).values()) if placa else []
        
        # Almacenamiento
        componentes['almacenamiento'] = list(Almacenamiento.objects.filter(id_chasis=pc.id_chasis).values())
        
        # Lector (relación 1-1)
        try:
            componentes['lector'] = model_to_dict(Lector.objects.get(id_chasis=pc.id_chasis))
        except Lector.DoesNotExist:
            componentes['lector'] = None
        
        # Fuente (relación 1-1)
        try:
            componentes['fuente'] = model_to_dict(Fuente.objects.get(id_chasis=pc.id_chasis))
        except Fuente.DoesNotExist:
            componentes['fuente'] = None
        
        # Combinar todos los datos
        snapshot_data = {**datos_base, 'componentes': componentes}
        
        # Convertir fechas recursivamente
        snapshot_data = convertir_fechas(snapshot_data)
        
        # Crear registro histórico
        ExpedienteHistorico.objects.create(
            pc=pc,
            datos_json=snapshot_data
        )
        
    except Exception as e:
        logger.error(f"Error creando snapshot para {pc}: {str(e)}")
        raise

def procesar_pc(data):
    with transaction.atomic():
        pc, created = procesar_pc_base(data)
        #created = false cuando se actualiza, true cuando hay q crearlo
        if created:
            crear_componentes(pc, data )
            crear_snapshot_historico(pc)
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
    #created = false cuando se actualiza, true cuando hay q crearlo
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
    # Lector
    for lector in data['cdrom_drives']:
        Lector.objects.create(
            desc_lector=lector['id'],
            tipo_lector=lector['hwid'],
            id_chasis=pc.id_chasis
        )
        
    for ranura in data['slots']:
        Ranura_Expansion.objects.create(
            id_slot=ranura['id'],
            uso=ranura['status'],
            id_chasis=pc.id_chasis
        )

def actualizar_componentes(pc, data):
    with transaction.atomic():
        cambios = detectar_cambios(pc, data)
        #print ('cambios >>>>',cambios)
        if cambios:
            crear_snapshot_historico(pc)
            aplicar_cambios_componentes(pc, data)  
            registrar_incidencia(pc, cambios)
        # Actualizar fecha siempre
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
    
    # Comparar componentes hardware
    
    # RAM
    rams_nuevas = len(new_data['memory'])
    rams_viejas = Ram.objects.filter(id_placa__id_chasis=pc.id_chasis)
    
    if rams_nuevas != rams_viejas:
        cambios[f'Rams'] = 'Cambio en Unidades Ram'
    else:
        for i, ram_nueva in enumerate(new_data['memory']):
            if i < len(rams_viejas):
                ram_vieja = rams_viejas[i]
                if ram_vieja.no_serie_ram != ram_nueva['serial']:
                    cambios[f'RAM_{i}'] = f"Serial cambió {ram_vieja.no_serie_ram} -> {ram_nueva['serial']}"
            else:
                cambios[f'RAM_{i}'] = f"RAM nueva detectada: {ram_nueva['serial']}"

    # Almacenamiento
    alm_nuevos = len(new_data['hard_drives'])
    almacenamientos_viejos = Almacenamiento.objects.filter(id_chasis=pc.id_chasis)
    if alm_nuevos != len(almacenamientos_viejos):
        cambios[f'Almacenamiento'] = 'Cambio en Unidades de Almacenamiento'
    else:
        almacenamientos_viejos = Almacenamiento.objects.filter(id_chasis=pc.id_chasis)
        for i, almacenamiento_nuevo in enumerate(new_data['hard_drives']):
            if i < len(almacenamientos_viejos):
                almacenamiento_viejo = almacenamientos_viejos[i]
                if (almacenamiento_viejo.modelo_alm != almacenamiento_nuevo['model'] or
                    almacenamiento_viejo.no_serie_alm != almacenamiento_nuevo['serial'] or
                    almacenamiento_viejo.tipo_alm != almacenamiento_nuevo['interface'] or
                    almacenamiento_viejo.capacidad_alm != almacenamiento_nuevo['size_gb'] * 1024 ):
                    cambios[f'Almacenamiento_{i}'] = (
                        f"Modelo: {almacenamiento_viejo.modelo_alm} -> {almacenamiento_nuevo['model']}, "
                        f"Serial: {almacenamiento_viejo.no_serie_alm} -> {almacenamiento_nuevo['serial']}, "
                        f"Tipo: {almacenamiento_viejo.tipo_alm} -> {almacenamiento_nuevo['interface']}, "
                        f"Capacidad: {almacenamiento_viejo.capacidad_alm} -> {almacenamiento_nuevo['size_gb']}"
                    )
            else:
                cambios[f'Almacenamiento_{i}'] = f"Almacenamiento nuevo detectado: {almacenamiento_nuevo['model']}"

    # Procesador
    procesador_viejo = Procesador.objects.get(id_placa__id_chasis=pc.id_chasis)
    procesador_nuevo = new_data['cpus'][0]
    if (procesador_viejo.desc_procesador != procesador_nuevo['name'] or
        procesador_viejo.velocidad_procesador != procesador_nuevo['clock'] or
        procesador_viejo.arq_procesador != (str(procesador_nuevo['cores']) + ' cores')):
        cambios['Procesador'] = (
            f"Descripción: {procesador_viejo.desc_procesador} -> {procesador_nuevo['name']}, "
            f"Velocidad: {procesador_viejo.velocidad_procesador} -> {procesador_nuevo['clock']} MHz, "
            f"Núcleos: {procesador_viejo.arq_procesador} -> {procesador_nuevo['cores']} cores"
        )

    # Placa Base
    placa_base_vieja = Placa_Base.objects.all().filter(id_chasis=pc.id_chasis)[0]
    placa_nueva = new_data['motherboards'][0]
    if (placa_base_vieja.fabricante_placa != placa_nueva['manufacturer'] or
        placa_base_vieja.modelo_placa != placa_nueva['product'].strip() or
        placa_base_vieja.no_serie_placa != placa_nueva['serial']):
        cambios['Placa Base'] = (
            f"Fabricante: {placa_base_vieja.fabricante_placa} -> {placa_nueva['manufacturer']}, "
            f"Modelo: {placa_base_vieja.modelo_placa} -> {placa_nueva['product']}, "
            f"Serial: {placa_base_vieja.no_serie_placa} -> {placa_nueva['serial']}"
        )
    
    # Tarjeta de Red
    tarjetas_red_viejas = Tarjeta_Red.objects.filter(id_placa__id_chasis=pc.id_chasis)

    # Mapear tarjetas viejas por MAC (si existe)
    viejas_por_mac = {tarjeta.mac: tarjeta for tarjeta in tarjetas_red_viejas if tarjeta.mac != 'N/A'}

    for i, tarjeta_red_nueva in enumerate(new_data['network_adapters']):
        if tarjeta_red_nueva.get('mac', 'N/A') != 'N/A' and tarjeta_red_nueva.get('ip', 'N/A') != 'N/A':
            mac_nueva = tarjeta_red_nueva.get('mac', 'Sin MAC')
            
            if mac_nueva in viejas_por_mac:
                tarjeta_vieja = viejas_por_mac[mac_nueva]
                cambios_detectados = False
                cambios_texto = []
                
                # Comparar campos
                if tarjeta_vieja.ip != tarjeta_red_nueva.get('ip', 'N/A'):
                    cambios_texto.append(f"IP: {tarjeta_vieja.ip} -> {tarjeta_red_nueva.get('ip', 'N/A')}")
                    cambios_detectados = True
                
                if tarjeta_vieja.subnet != tarjeta_red_nueva.get('subnet', 'N/A'):
                    cambios_texto.append(f"Subred: {tarjeta_vieja.subnet} -> {tarjeta_red_nueva.get('subnet', 'N/A')}")
                    cambios_detectados = True
                
                if tarjeta_vieja.gateway != tarjeta_red_nueva.get('gateway', 'N/A'):
                    cambios_texto.append(f"Gateway: {tarjeta_vieja.gateway} -> {tarjeta_red_nueva.get('gateway', 'N/A')}")
                    cambios_detectados = True
                
                if cambios_detectados:
                    cambios[f'Tarjeta Red {mac_nueva}'] = ", ".join(cambios_texto)
            else:
                cambios[f'Tarjeta Red {mac_nueva}'] = f"Nueva tarjeta detectada (MAC: {mac_nueva})"

    
    # Lector
    try:
        lector_viejo = Lector.objects.get(id_chasis=pc.id_chasis)
        if 'cdrom_drives' in new_data and new_data['cdrom_drives']:
            lector_nuevo = new_data['cdrom_drives'][0]
            if (lector_viejo.desc_lector != lector_nuevo.get('id', '') or
                lector_viejo.tipo_lector != lector_nuevo.get('hwid', '')):
                cambios['Lector'] = (
                    f"Descripción: {lector_viejo.desc_lector} -> {lector_nuevo.get('id', 'No especificado')}, "
                    f"Tipo: {lector_viejo.tipo_lector} -> {lector_nuevo.get('hwid', 'No especificado')}"
                )
    except Lector.DoesNotExist:
        if 'cdrom_drives' in new_data and new_data['cdrom_drives']:
            lector_nuevo = new_data['cdrom_drives'][0]
            cambios['Lector'] = f"Lector nuevo detectado: {lector_nuevo.get('description', 'No especificado')}"

    
    # Ranuras de Expansión
    ranuras_viejas = Ranura_Expansion.objects.filter(id_chasis=pc.id_chasis)
    for i, ranura_nueva in enumerate(new_data['slots']):
        if i < len(ranuras_viejas):
            ranura_vieja = ranuras_viejas[i]
            if (ranura_vieja.id_slot != ranura_nueva['id'] or
                ranura_vieja.uso != ranura_nueva['status']):
                cambios[f'Ranura {i}'] = (
                    f"ID: {ranura_vieja.id_slot} -> {ranura_nueva['id']}, "
                    f"Uso: {ranura_vieja.uso} -> {ranura_nueva['status']}"
                )
        else:
            cambios[f'Ranura {i}'] = f"Ranura nueva detectada: {ranura_nueva['id']}"

    # Periféricos
    perifericos_viejos = Perifericos.objects.filter(id_pc=pc)
    for i, periferico_nuevo in enumerate(new_data.get('peripherals', [])):
        if i < len(perifericos_viejos):
            periferico_viejo = perifericos_viejos[i]
            if (periferico_viejo.tipo_periferico != periferico_nuevo.get('type', '') or
                periferico_viejo.modelo_periferico != periferico_nuevo.get('model', '') or
                periferico_viejo.no_serie_periferico != periferico_nuevo.get('serial', '')):
                cambios[f'Periférico {i}'] = (
                    f"Tipo: {periferico_viejo.tipo_periferico} -> {periferico_nuevo.get('type', 'No especificado')}, "
                    f"Modelo: {periferico_viejo.modelo_periferico} -> {periferico_nuevo.get('model', 'No especificado')}, "
                    f"Serial: {periferico_viejo.no_serie_periferico} -> {periferico_nuevo.get('serial', 'No especificado')}"
                )
        else:
            cambios[f'Periférico {i}'] = f"Periférico nuevo detectado: {periferico_nuevo.get('type', 'No especificado')}"

    return cambios

def registrar_incidencia(pc, cambios):
    desc = "Cambios detectados:\n" + "\n".join([f"{k}: {v}" for k, v in cambios.items()])
    
    Incidencias.objects.create(
        desc_incidencia="Modificación de hardware",
        fecha_incidencia=datetime.now().date(),
        observacion=desc[:250], 
        id_pc=pc
    )

def obtener_entidad(segmento):
    # Buscar en el diccionario
    entrada = MAPEO_ENTIDADES.get(segmento, None)
    
    if entrada:
        return {'nombre': entrada[0], 'tipo': entrada[1]}
    else:
        return {'nombre': segmento, 'tipo': 'Otros'}

def aplicar_cambios_componentes(pc, new_data):
    try:
        with transaction.atomic():
            placa = Placa_Base.objects.get(id_chasis=pc.id_chasis)
            chasis = pc.id_chasis

            # Actualizar Placa Base
            placa_data = new_data['motherboards'][0]
            Placa_Base.objects.filter(id_placa=placa.id_placa).update(
                fabricante_placa=placa_data['manufacturer'],
                modelo_placa=placa_data['product'].strip(),
                no_serie_placa=placa_data['serial'].strip()
            )

            # Actualizar Procesador
            cpu_data = new_data['cpus'][0]
            Procesador.objects.filter(id_placa=placa).update(
                desc_procesador=cpu_data['name'],
                velocidad_procesador=cpu_data['clock'],
                arq_procesador=f"{cpu_data['cores']} cores"
            )

            # Actualizar RAMs (eliminar antiguas y crear nuevas)
            Ram.objects.filter(id_placa=placa).delete()
            for mem in new_data['memory']:
                Ram.objects.create(
                    capacidad_ram=mem['capacity_gb'],
                    no_serie_ram=mem['serial'],
                    tipo_ram=f"DDR{mem['type_code']}",
                    id_placa=placa
                )
                
            # Actualizar ranuras (eliminar antiguas y crear nuevas)
            Ranura_Expansion.objects.filter(id_chasis=chasis).delete()
            for ranura in new_data['slots']:
                Ranura_Expansion.objects.create(
                    id_slot=ranura['id'],
                    uso=ranura['status'],
                    id_chasis=chasis
                )

            # Actualizar Almacenamiento
            Almacenamiento.objects.filter(id_chasis=chasis).delete()
            for hdd in new_data['hard_drives']:
                Almacenamiento.objects.create(
                    no_serie_alm=hdd['serial'],
                    tipo_alm=hdd['interface'],
                    interface_alm=hdd['model'],
                    modelo_alm=hdd['model'],
                    capacidad_alm=hdd['size_gb'] * 1024,
                    id_chasis=chasis
                )

            # Actualizar Tarjetas de Red
            Tarjeta_Red.objects.filter(id_placa=placa).delete()
            for adapter in new_data['network_adapters']:
                if adapter['ip'] != 'N/A':
                    Tarjeta_Red.objects.create(
                        mac=adapter['mac'],
                        ip=adapter['ip'],
                        subnet=adapter['subnet'],
                        gateway=adapter['gateway'],
                        id_placa=placa
                    )
                    
            #Actualizar lector
            lec_data = new_data['cdrom_drives']
            if lec_data:
                Lector.objects.filter(id_chasis=chasis).update(
                    desc_lector=lec_data['id'],
                    tipo_lector=lec_data['hwid'],
                )
            else:
                pass
            
            # Actualizar PC
            Pc.objects.filter(id_pc=pc.id_pc).update(
                nombre_equipo=new_data['pc_name'],
                so=new_data['operating_systems'][0]['version']
            )

            logger.info(f"Componentes actualizados para {pc.nombre_equipo}")

    except Exception as e:
        logger.error(f"Error actualizando componentes de {pc}: {str(e)}")
        raise

MAPEO_ENTIDADES = { 
    # Complejos 
    
    # agregar nomencladores de municipios
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