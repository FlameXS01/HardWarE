
import ftplib
import pandas as pd
import os
import django
from django.conf import settings

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # Cambia 'tu_proyecto' por el nombre de tu proyecto
django.setup()

# Importar tu modelo
from Storage.models import EjemploModel  #modelos

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

        # Guardar los datos en la base de datos
        for index, row in df.iterrows():
            # Suponiendo que tu modelo tiene tres campos: nombre1, nombre2, nombre3
            ejemplo = EjemploModel(
                nombre1=row['nombre1'],  # Cambia 'nombre1' por el nombre de la columna en tu Excel
                nombre2=row['nombre2'],  # Cambia 'nombre2' por el nombre de la columna en tu Excel
                nombre3=row['nombre3']   # Cambia 'nombre3' por el nombre de la columna en tu Excel
            )
            ejemplo.save()  # Guardar el objeto en la base de datos

        # Eliminar el archivo local después de procesarlo
        os.remove(file)

# Cerrar la conexión FTP
ftp.quit()