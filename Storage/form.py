from django import forms
from .models import *
from django.contrib.auth.models import User

class PcForm(forms.ModelForm):
    class Meta:
        model = Pc
        fields = ['so', 'nombre_equipo', 'ultimo_reporte', 'id_chasis', 'serial_pc', 'id_entidad']
        widgets = {
            'so': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sistema Operativo', 'required': True}),
            'nombre_equipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Equipo', 'required': True}),
            'ultimo_reporte': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Último Reporte', 'required': True}),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'placeholder': 'Propietario anterior', 'required': True}),
            'serial_pc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial del Equipo', 'required': True}),
            'id_entidad': forms.Select(attrs={'class':'form-control', 'required': True}),
            }
        
    def __init__(self, *args, **kwargs):
        super(PcForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
        self.fields['id_entidad'].queryset = Entidad.objects.all()
class ChasisForm(forms.ModelForm):
    
    nombre_equipo = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = Chasis
        fields = ['tipo_chasis','nombre_equipo']
        widgets = {
            'tipo_chasis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Chasis', 'required': True}),
            'pc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PC', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  
            self.initial['nombre_equipo'] = self.instance.nombre_equipo_relacionado
class LectorForm(forms.ModelForm):
    class Meta:
        model = Lector
        fields = ['desc_lector', 'tipo_lector', 'id_chasis'] 
        widgets = {
            'desc_lector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del Lector', 'required': True}),
            'tipo_lector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Lector', 'required': True}),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'placeholder': 'Propietario anterior', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(LectorForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
class AlmacenamientoForm(forms.ModelForm):
    class Meta:
        model = Almacenamiento
        fields = ['no_serie_alm','tipo_alm','interface_alm','modelo_alm','capacidad_alm','id_chasis']
        widgets = {
            'no_serie_alm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Número de Serie', 'required': True}),
            'tipo_alm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Tipo de Almacenamiento', 'required': True}),
            'interface_alm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Interfaz', 'required': True}),
            'modelo_alm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Modelo', 'required': True}),
            'capacidad_alm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Capacidad', 'required': True}),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'placeholder': 'Propietario anterior', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(AlmacenamientoForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
class PlacaBaseForm(forms.ModelForm):
    class Meta:
        model = Placa_Base
        fields = ['no_serie_placa', 'fabricante_placa', 'modelo_placa', 'id_chasis']
        widgets = {
            'no_serie_placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Serie', 'required': True}),
            'fabricante_placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabricante', 'required': True}),
            'modelo_placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo', 'required': True}),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'placeholder': 'Propietario anterior', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(PlacaBaseForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
class ProcesadorForm(forms.ModelForm):
    class Meta:
        model = Procesador
        fields = ['desc_procesador', 'velocidad_procesador','arq_procesador', 'id_placa']
        widgets = {
            'desc_procesador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del Procesador', 'required': True}),
            'velocidad_procesador': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Velocidad del Procesador (MHz)', 'required': True}),
            #'conector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Conector', 'required': True}),
            'arq_procesador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Arquitectura del Procesador', 'required': True}),
            'id_placa': forms.Select(attrs={'class':'form-control', 'placeholder': 'Placa base', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(ProcesadorForm, self).__init__(*args, **kwargs)
        self.fields['id_placa'].queryset = Placa_Base.objects.all()
class RamForm(forms.ModelForm):
    class Meta:
        model = Ram
        fields = ['capacidad_ram', 'no_serie_ram', 'tipo_ram', 'id_placa']
        widgets = {
            'capacidad_ram': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad de la RAM (GB)', 'required': True}),
            'no_serie_ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Serie de la RAM', 'required': True}),
            'tipo_ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de RAM', 'required': True}),
            'id_placa': forms.Select(attrs={'class':'form-control', 'placeholder': '----', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(RamForm, self).__init__(*args, **kwargs)
        self.fields['id_placa'].queryset = Placa_Base.objects.all()
class TarjetaRedForm(forms.ModelForm):
    class Meta:
        model = Tarjeta_Red
        fields = ['mac', 'ip', 'subnet', 'gateway', 'id_placa']
        widgets = {
            'mac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección MAC', 'required': True}),
            'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección IP', 'required': True}),
            'subnet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subred', 'required': True}),
            'gateway': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gateway', 'required': True}),
            'id_placa': forms.Select(attrs={'class':'form-control', 'placeholder': '----', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(TarjetaRedForm, self).__init__(*args, **kwargs)
        self.fields['id_placa'].queryset = Placa_Base.objects.all()
class Ranura_ExpansionForm(forms.ModelForm):
    class Meta:
        model = Ranura_Expansion
        fields = ['id_slot', 'uso', 'id_chasis']
        widgets = {
            'id_slot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slot', 'required': True}),
            'uso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uso', 'required': True}),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(Ranura_ExpansionForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
class FuenteForm(forms.ModelForm):
    class Meta:
        model = Fuente
        fields = ['fabricante_fuente', 'no_serie_fuente', 'potencia_fuente', 'id_chasis']
        widgets = {
            'fabricante_fuente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabricante', 'required': True}),
            'no_serie_fuente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Serie', 'required': True},),
            'potencia_fuente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Potencia', 'required': True},),
            'id_chasis': forms.Select(attrs={'class':'form-control', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(FuenteForm, self).__init__(*args, **kwargs)
        self.fields['id_chasis'].queryset = Chasis.objects.all()
class PerifericosForm(forms.ModelForm):
    class Meta:
        model = Perifericos
        fields = ['tipo_periferico', 'no_serie_periferico', 'fabricante_periferico', 'modelo_periferico', 'id_pc']
        widgets = {
            'tipo_periferico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de Periférico', 'required': True}),
            'no_serie_periferico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Serie del Periférico', 'required': True}),
            'fabricante_periferico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fabricante del Periférico', 'required': True}),
            'modelo_periferico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo del Periférico', 'required': True}),
            'id_pc': forms.Select(attrs={'class':'form-control', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(PerifericosForm, self).__init__(*args, **kwargs)
        self.fields['id_pc'].queryset = Pc.objects.all() 
class IncidenciasForm(forms.ModelForm):
    class Meta: 
        model = Incidencias
        fields = ['observacion','desc_incidencia','fecha_incidencia', 'id_pc']
        widgets = {
            'observacion': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Observación', 'required': True}),
            'desc_incidencia': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Descripción', 'required': True}),
            'fecha_incidencia': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'Fecha de la incidencia', 'required': True}),
            'id_pc': forms.Select(attrs={'class':'form-control', 'required': True}),
        }
    def __init__(self, *args, **kwargs):
        super(IncidenciasForm, self).__init__(*args, **kwargs)
        self.fields['id_pc'].queryset = Pc.objects.all() 
class EntidadForm(forms.ModelForm):
    class Meta: 

        model = Entidad
        fields = ['tipoEntidad', 'nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre', 'required': True}),
            'tipoEntidad': forms.Select(
                attrs={'class':'form-control', 'required': True},
                choices=[ 
                    ('Complejo', 'Complejo'),
                    ('UEB', 'UEB'),
                    ('Otro', 'Otro'),
                ]
            ),
        }

    class Meta: 

        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre', 'required': True}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '*********', 'required': True})
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre de usuario','required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre','required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido','required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico','required': True}),
            'is_superuser': forms.Select(
                attrs={'class': 'form-control','required': True},
                choices=[
                    (True, 'Superusuario'),
                    (False, 'Usuario estándar')
                ]
            ),
        }
