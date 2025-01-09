import ftplib
import pandas as pd
import os
import django
from django.conf import settings

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # Cambia 'tu_proyecto' por el nombre de tu proyecto
django.setup()

# Importar tus modelos
from Storage.models import Chasis, Pc, Lector, Ranura_Expansion, Almacenamiento, Placa_Base, Procesador, Ram, Tarjeta_Red, Fuente, Perifericos, Incidencias

# Configuración del servidor FTP
FTP_SERVER = 'ftp.ejemplo.com'  # Cambia esto a tu servidor FTP
FTP_USER = 'tu_usuario'          # Cambia esto a tu usuario FTP
FTP_PASS = 'tu_contraseña'       # Cambia esto a tu contraseña FTP
REMOTE_DIR = '/Uploads/'         # Cambia esto a la carpeta donde se suben los archivos

# Conectar al servidor FTP
ftp = ftplib.FTP(FTP_SERVER)
ftp.login(FTP_USER, FTP_PASS)

# Cambiar al directorio remoto
ftp.cwd(REMOTE_DIR)

# Listar archivos en el directorio remoto
files = ftp.nlst()

# Procesar cada archivo Excel
for file in files:
    if file.endswith('.xlsx'):  # Filtrar solo archivos Excel
        # Leer el archivo Excel directamente desde el FTP
        with open(file, 'wb') as local_file:
            ftp.retrbinary(f'RETR {file}', local_file.write)

        # Cargar el archivo Excel en un DataFrame
        df = pd.read_excel(file)

        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            # Crear o obtener el chasis
            chasis, created = Chasis.objects.get_or_create(
                ultimo_propietario=row['ultimo_propietario'],  # Cambia según tu Excel
                tipo_chasis=row['tipo_chasis']  # Cambia según tu Excel
            )

            # Crear o actualizar la PC
            pc, created = Pc.objects.update_or_create(
                nombre_equipo=row['nombre_equipo'],  # Cambia según tu Excel
                defaults={
                    'so': row['so'],  # Cambia según tu Excel
                    'ultimo_reporte': row['ultimo_reporte'],  # Cambia según tu Excel
                    'id_chasis': chasis
                }
            )

            if created:
                print(f"Se creó una nueva PC: {pc.nombre_equipo}")
            else:
                print(f"Se actualizó la PC existente: {pc.nombre_equipo}")

            # Crear o actualizar otros modelos según sea necesario
            # Por ejemplo, para el almacenamiento
            
            if 'no_serie_alm' in row and pd.notna(row['no_serie_alm']):
                Almacenamiento.objects.update_or_create(
                    no_serie_alm=row['no_serie_alm'],  # Cambia según tu Excel
                    id_chasis=chasis,
                    defaults={
                        'tipo_alm': row['tipo_alm'],  # Cambia según tu Excel
                        'interface_alm': row['interface_alm'],  # Cambia según tu Excel
                        'modelo_alm': row['modelo_alm'],  # Cambia según tu Excel
                        'capacidad_alm': row['capacidad_alm']  # Cambia según tu Excel
                    }
                )

            # Repite el proceso para otros modelos como RAM, Procesador, etc.
            if 'no_serie_ram' in row and pd.notna(row['no_serie_ram']):
                Ram.objects.update_or_create(
                    no_serie_ram=row['no_serie_ram'],  # Cambia según tu Excel
                    id_placa=pc.id_chasis.placa_base,  # Asegúrate de que la relación sea correcta
                    defaults={
                        'capacidad_ram': row['capacidad_ram'],  # Cambia según tu Excel
                        'tipo_ram': row['tipo_ram']  # Cambia según tu Excel
                    }
                )

            # Agrega más lógica para otros componentes como Lector, Ranura_Expansion, etc.

        # Eliminar el archivo local después de procesarlo
        os.remove(file)

# Cerrar la conexión FTP
ftp.quit()
