from django.shortcuts import render,redirect
from Storage.form import*
from Storage.models import*
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

    #index view 
def index(request):
    # Obtener todas las PCs y las incidencias
    pcs = Pc.objects.all()
    incidencias = Incidencias.objects.all()
    
    # Contar la cantidad total de PCs
    cont = pcs.count()
    # Contar la cantidad de PCs por entidad
    pcs_por_entidad = pcs.values('id_entidad__nombre').annotate(count=Count('id_entidad')).order_by()
    
    # Contar la cantidad de modelos de placas
    modelos_placas = Placa_Base.objects.values('modelo_placa').annotate(count=Count('modelo_placa')).order_by()
    # Preparar los datos para el gráfico de barras (Cantidad de PCs por Entidad)
    entidades_labels = [entidad['id_entidad__nombre'] for entidad in pcs_por_entidad]
    entidades_values = [entidad['count'] for entidad in pcs_por_entidad]
    # Preparar los datos para el gráfico de pastel (Cantidad de Modelos de Placas)
    placas_labels = [placa['modelo_placa'] for placa in modelos_placas]
    placas_values = [placa['count'] for placa in modelos_placas]
    context = {
        'pcs': pcs,
        'incidencias': incidencias,
        'cont': cont,
        'entidades_labels': entidades_labels,
        'entidades_values': entidades_values,
        'placas_labels': placas_labels,
        'placas_values': placas_values,
    }
    return render(request, 'base/index.html', context)

#=================================> Pc <======================================#

    #LISTAR PC  
def list_pc(request):
    pc = Pc.objects.all()
    return render(request,'Pc/list_pc.html',{"pcs":pc})

    #ADD PC
def add_pc(request): 
    pc_form = PcForm()
    
    if request.method == 'POST':
        pc_form = PcForm(data = request.POST)
        if pc_form.is_valid():
            #guardar el pc
            pc_form.save()
            return redirect('list_pc')
    
    return render(request, 'Pc/add_pc.html',{'pc_form':pc_form})


    #EDIT PC
def edit_pc(request, id_pc):
    pc = Pc.objects.get(id_pc=id_pc)
    pc_form = PcForm(instance=pc)
    
    if request.method == 'POST':
        pc_form = PcForm(request.POST, instance = pc)
        if pc_form.is_valid():
            pc_form.save()
            return redirect('list_pc')
    return render(request, 'Pc/edit_pc.html',{'pc_form': pc_form})


    #DELETE_PC
def del_pc(request, id_pc):
    pc_to_delete = Pc.objects.get(pk = id_pc)
    pc_to_delete.delete()
    
    return redirect('list_pc')

#=================================> Chasis <======================================#

    #LISTAR CHASIS  
def list_chasis(request):
    chasis = Chasis.objects.all().select_related('pc')
    return render(request,'Chasis/list_chasis.html',{"chasis":chasis})

    #ADD CHASIS
def add_chasis(request): 
    chasis_form = ChasisForm()
    
    if request.method == 'POST':
        chasis_form = ChasisForm(data = request.POST)
        if chasis_form.is_valid():
            #guardar el chasis
            chasis_form.save()
            return redirect('list_chasis')
    
    return render(request, 'Chasis/add_chasis.html',{'chasis_form':chasis_form})


    #EDIT CHASIS
def edit_chasis(request, id_chasis):
    chasis = Chasis.objects.get(id_chasis=id_chasis)
    chasis_form = ChasisForm(instance=chasis)
    
    if request.method == 'POST':
        chasis_form = ChasisForm(request.POST, instance = chasis)
        if chasis_form.is_valid():
            chasis_form.save()
            return redirect('list_chasis')
    return render(request, 'Chasis/edit_chasis.html',{'chasis_form': chasis_form})


    #DELETE CHASIS
def del_chasis(request, id_chasis):
    chasis_to_delete = Chasis.objects.get(pk = id_chasis)
    chasis_to_delete.delete()
    
    return redirect('list_chasis')

#=================================> Incidencia <======================================#            
            
    #LISTAR INCIDENCIA
def list_incidencia(request):
    incidencias = Incidencias.objects.all() 
    return render(request, 'Incidencia/list_incidencia.html', {'incidencias': incidencias})

    #ADD INCIDENCIA
def add_incidencia(request):
    incidencia_form = IncidenciasForm()
    
    if request.method == 'POST':
        incidencia_form = IncidenciasForm(data = request.POST)
        if incidencia_form.is_valid():
            #guardar el incidencia
            incidencia_form.save()
            return redirect('list_incidencia')
    
    return render(request, 'Incidencia/add_incidencia.html',{'incidencia_form':incidencia_form})
    
    #EDIT INCIDENCIA
def edit_incidencia(request, id_incidencia):
    incidencia = Incidencias.objects.get(id_incidencia=id_incidencia)
    incidencia_form = IncidenciasForm(instance=incidencia)
    
    if request.method == 'POST':
        incidencia_form = IncidenciasForm(request.POST, instance = incidencia)
        if incidencia_form.is_valid():
            incidencia_form.save()
            return redirect('list_incidencia')
    return render(request, 'Incidencia/edit_incidencia.html',{'incidencia_form': incidencia_form})

    #DELETE INCIDENCIA
def del_incidencia(request, id_incidencia):
    incidencia_to_delete = Incidencias.objects.get(pk = id_incidencia)
    incidencia_to_delete.delete()
    
    return redirect('list_incidencia')

#==========================================> Periféricos <============================================#
            
    #LISTAR Periféricos
def list_periferico(request):
    perifericos = Perifericos.objects.all() 
    return render(request, 'Periferico/list_periferico.html', {'perifericos': perifericos})

    #ADD Periféricos
def add_periferico(request):
    periferico_form = PerifericosForm()
    
    if request.method == 'POST':
        periferico_form = PerifericosForm(data = request.POST)
        if periferico_form.is_valid():
            #guardar el periferico
            periferico_form.save()
            return redirect('list_periferico')
    
    return render(request, 'Periferico/add_periferico.html',{'periferico_form':periferico_form})
    
    #EDIT Periféricos
def edit_periferico(request, id_periferico):
    periferico = Perifericos.objects.get(id_periferico=id_periferico)
    periferico_form = PerifericosForm(instance=periferico)
    
    if request.method == 'POST':
        periferico_form = PerifericosForm(request.POST, instance = periferico)
        if periferico_form.is_valid():
            periferico_form.save()
            return redirect('list_periferico')
    return render(request, 'Periferico/edit_periferico.html',{'periferico_form': periferico_form})

    #DELETE Periféricos
def del_periferico(request, id_periferico):
    periferico_to_delete = Perifericos.objects.get(pk = id_periferico)
    periferico_to_delete.delete()
    
    return redirect('list_periferico')

#==========================================> Fuente <============================================#
            
    #LISTAR FUENTE
def list_fuente(request):
    fuentes = Fuente.objects.all() 
    return render(request, 'Fuente/list_fuente.html', {'fuentes': fuentes})

    #ADD FUENTE
def add_fuente(request):
    fuente_form = FuenteForm()
    
    if request.method == 'POST':
        fuente_form = FuenteForm(data = request.POST)
        if fuente_form.is_valid():
            #guardar el periferico
            fuente_form.save()
            return redirect('list_fuente')
    
    return render(request, 'Fuente/add_fuente.html',{'fuente_form':fuente_form})
    
    #EDIT FUENTE
def edit_fuente(request, id_fuente):
    fuente = Fuente.objects.get(id_fuente=id_fuente)
    fuente_form = FuenteForm(instance=fuente)
    
    if request.method == 'POST':
        fuente_form = FuenteForm(request.POST, instance = fuente)
        if fuente_form.is_valid():
            fuente_form.save()
            return redirect('list_fuente')
    return render(request, 'Fuente/edit_fuente.html',{'fuente_form': fuente_form})

    #DELETE FUENTE
def del_fuente(request, id_fuente):
    fuente_to_delete = Fuente.objects.get(pk = id_fuente)
    fuente_to_delete.delete()
    
    return redirect('list_fuente')

#==========================================> Almacenamiento <============================================#
            
    #LISTAR Almacenamiento
def list_almacenamiento(request):
    almacenamientos = Almacenamiento.objects.all() 
    return render(request, 'Almacenamiento/list_almacenamiento.html', {'almacenamientos': almacenamientos})

    #ADD Almacenamiento
def add_almacenamiento(request):
    almacenamiento_form = AlmacenamientoForm()
    
    if request.method == 'POST':
        almacenamiento_form = AlmacenamientoForm(data = request.POST)
        if almacenamiento_form.is_valid():
            #guardar el almacenamiento
            almacenamiento_form.save()
            return redirect('list_almacenamiento')
    
    return render(request, 'Almacenamiento/add_almacenamiento.html',{'almacenamiento_form':almacenamiento_form})
    
    #EDIT Almacenamiento
def edit_almacenamiento(request, id_almacenamiento):
    almacenamiento = Almacenamiento.objects.get(id_almacenamiento=id_almacenamiento)
    almacenamiento_form = AlmacenamientoForm(instance=almacenamiento)
    
    if request.method == 'POST':
        almacenamiento_form = AlmacenamientoForm(request.POST, instance = almacenamiento)
        if almacenamiento_form.is_valid():
            almacenamiento_form.save()
            return redirect('list_almacenamiento')
    return render(request, 'Almacenamiento/edit_almacenamiento.html',{'almacenamiento_form': almacenamiento_form})

    #DELETE Almacenamiento
def del_almacenamiento(request, id_almacenamiento):
    almacenamiento_to_delete = Almacenamiento.objects.get(pk = id_almacenamiento)
    almacenamiento_to_delete.delete()
    
    return redirect('list_almacenamiento')

#==========================================> Procesador <============================================#
            
    #LISTAR Procesador
def list_procesador(request):
    procesadores = Procesador.objects.all() 
    return render(request, 'Procesador/list_procesador.html', {'procesadores': procesadores})

    #ADD Procesador
def add_procesador(request):
    procesador_form = ProcesadorForm()
    
    if request.method == 'POST':
        procesador_form = ProcesadorForm(data = request.POST)
        if procesador_form.is_valid():
            #guardar el Procesador
            procesador_form.save()
            return redirect('list_procesador')
    
    return render(request, 'Procesador/add_procesador.html',{'procesador_form':procesador_form})
    
    #EDIT Procesador
def edit_procesador(request, id_procesador):
    procesador = Procesador.objects.get(id_procesador=id_procesador)
    procesador_form = ProcesadorForm(instance=procesador)
    
    if request.method == 'POST':
        procesador_form = ProcesadorForm(request.POST, instance = procesador)
        if procesador_form.is_valid():
            procesador_form.save()
            return redirect('list_procesador')
    return render(request, 'Procesador/edit_procesador.html',{'procesador_form': procesador_form})

    #DELETE Procesador
def del_procesador(request, id_procesador):
    procesador_to_delete = Procesador.objects.get(pk = id_procesador)
    procesador_to_delete.delete()
    
    return redirect('list_procesador')

#==========================================> Placa Base <============================================#
            
    #LISTAR Placa
def list_placa(request):
    placas = Placa_Base.objects.all() 
    return render(request, 'Placa_Base/list_placa.html', {'placas': placas})

    #ADD Placa
def add_placa(request):
    placa_form = PlacaBaseForm()
    
    if request.method == 'POST':
        placa_form = PlacaBaseForm(data = request.POST)
        if placa_form.is_valid():
            #guardar la Placa
            placa_form.save()
            return redirect('list_placa')
    
    return render(request, 'Placa_Base/add_placa.html',{'placa_form':placa_form})
    
    #EDIT Placa
def edit_placa(request, id_placa):
    placa = placa.objects.get(id_placa=id_placa)
    placa_form = PlacaBaseForm(instance=placa)
    
    if request.method == 'POST':
        placa_form = PlacaBaseForm(request.POST, instance = placa)
        if placa_form.is_valid():
            placa_form.save()
            return redirect('list_placa')
    return render(request, 'Placa_Base/edit_placa.html',{'placa_form': placa_form})

    #DELETE Placa
def del_placa(request, id_placa):
    placa_to_delete = Placa_Base.objects.get(pk = id_placa)
    placa_to_delete.delete()
    
    return redirect('list_placa')

#==========================================> RAM <============================================#
            
    #LISTAR Ram
def list_ram(request):
    rams = Ram.objects.all() 
    return render(request, 'Ram/list_ram.html', {'rams': rams})

    #ADD Ram
def add_ram(request):
    ram_form = RamForm()
    
    if request.method == 'POST':
        ram_form = RamForm(data = request.POST)
        if ram_form.is_valid():
            #guardar la Ram
            ram_form.save()
            return redirect('list_ram')
    
    return render(request, 'Ram/add_ram.html',{'ram_form':ram_form})
    
    #EDIT Ram
def edit_ram(request, id_ram):
    ram = Ram.objects.get(id_ram=id_ram)
    ram_form = RamForm(instance=ram)
    
    if request.method == 'POST':
        ram_form = RamForm(request.POST, instance = ram)
        if ram_form.is_valid():
            ram_form.save()
            return redirect('list_ram')
    return render(request, 'Ram/edit_ram.html',{'ram_form': ram_form})

    #DELETE Ram
def del_ram(request, id_ram):
    ram_to_delete = Ram.objects.get(pk = id_ram)
    ram_to_delete.delete()
    
    return redirect('list_ram')

#==========================================> Lector <============================================#
            
    #LISTAR Lector
def list_lector(request):
    lectores = Lector.objects.all() 
    return render(request, 'Lector/list_lector.html', {'lectores': lectores})

    #ADD Lector
def add_lector(request):
    lector_form = LectorForm()
    
    if request.method == 'POST':
        lector_form = LectorForm(data = request.POST)
        if lector_form.is_valid():
            #guardar la Ram
            lector_form.save()
            return redirect('list_lector')
    
    return render(request, 'Lector/add_lector.html',{'lector_form':lector_form})
    
    #EDIT Lector
def edit_lector(request, id_lector):
    lector = Lector.objects.get(id_lector=id_lector)
    lector_form = LectorForm(instance=lector)
    
    if request.method == 'POST':
        lector_form = LectorForm(request.POST, instance = lector)
        if lector_form.is_valid():
            lector_form.save()
            return redirect('list_lector')
    return render(request, 'Lector/edit_lector.html',{'lector_form': lector_form})

    #DELETE Lector
def del_lector(request, id_lector):
    lector_to_delete = Lector.objects.get(pk = id_lector)
    lector_to_delete.delete()
    
    return redirect('list_lector')

#==========================================> Ranura Exp <============================================#
            
    #LISTAR Ranura Exp
def list_ranura(request):
    ranuras = Ranura_Expansion.objects.all() 
    return render(request, 'Ranura_Expansion/list_ranura.html', {'ranuras': ranuras})

    #ADD Ranura Exp
def add_ranura(request):
    ranura_form = Ranura_ExpansionForm()
    
    if request.method == 'POST':
        ranura_form = Ranura_ExpansionForm(data = request.POST)
        if ranura_form.is_valid():
            #guardar Ranura Exp
            ranura_form.save()
            return redirect('list_ranura')
    
    return render(request, 'Ranura_Expansion/add_ranura.html',{'ranura_form':ranura_form})
    
    #EDIT Ranura Exp
def edit_ranura(request, id_ranura):
    ranura = Ranura_Expansion.objects.get(id_ranura=id_ranura)
    ranura_form = Ranura_ExpansionForm(instance=ranura)
    
    if request.method == 'POST':
        ranura_form = Ranura_ExpansionForm(request.POST, instance = ranura)
        if ranura_form.is_valid():
            ranura_form.save()
            return redirect('list_ranura')
    return render(request, 'Ranura_Expansion/edit_ranura.html',{'ranura_form': ranura_form})

    #DELETE Ranura Exp
def del_ranura(request, id_ranura):
    ranura_to_delete = Ranura_Expansion.objects.get(pk = id_ranura)
    ranura_to_delete.delete()
    
    return redirect('list_ranura')

#==========================================> Tarjeta Red <============================================#
            
    #LISTAR Tarjeta Red
def list_tarjeta(request):
    tarjetas = Tarjeta_Red.objects.all() 
    return render(request, 'Tarjeta_Red/list_tarjeta.html', {'tarjetas': tarjetas})

    #ADD Tarjeta Red
def add_tarjeta(request):
    tarjeta_form = TarjetaRedForm()
    
    if request.method == 'POST':
        tarjeta_form = TarjetaRedForm(data = request.POST)
        if tarjeta_form.is_valid():
            #guardar Tarjeta Red
            tarjeta_form.save()
            return redirect('list_tarjeta')
    
    return render(request, 'Tarjeta_Red/add_tarjeta.html',{'tarjeta_form':tarjeta_form})
    
    #EDIT Tarjeta Red
def edit_tarjeta(request, id_tarjeta):
    tarjeta = Tarjeta_Red.objects.get(id_tarjeta=id_tarjeta)
    tarjeta_form = TarjetaRedForm(instance=tarjeta)
    
    if request.method == 'POST':
        tarjeta_form = TarjetaRedForm(request.POST, instance = tarjeta)
        if tarjeta_form.is_valid():
            tarjeta_form.save()
            return redirect('list_tarjeta')
    return render(request, 'Tarjeta_Red/edit_tarjeta.html',{'tarjeta_form': tarjeta_form})

    #DELETE Tarjeta Red
def del_tarjeta(request, id_tarjeta):
    tarjeta_to_delete = Tarjeta_Red.objects.get(pk = id_tarjeta)
    tarjeta_to_delete.delete()
    
    return redirect('list_tarjeta')

#=================================> Entidad <======================================#            
            
    #LISTAR Entidad
def list_entidad(request):
    entidades = Entidad.objects.all() 
    return render(request, 'Entidad/list_entidad.html', {'entidades': entidades})
def list_Complejo(request):
    entidades = Entidad.objects.filter(tipoEntidad='Complejo') 
    return render(request, 'Entidad/list_entidad.html', {'entidades': entidades})
def list_Ueb(request):
    entidades = Entidad.objects.filter(tipoEntidad='UEB')
    return render(request, 'Entidad/list_entidad.html', {'entidades': entidades})

    #ADD Entidad
def add_entidad(request):
    entidad_form = EntidadForm()
    
    if request.method == 'POST':
        entidad_form = EntidadForm(data = request.POST)
        if entidad_form.is_valid():
            #guardar la entidad
            entidad_form.save()
            return redirect('list_entidad')
    
    return render(request, 'Entidad/add_entidad.html',{'entidad_form':entidad_form})
    
    #EDIT entidad
def edit_entidad(request, id_entidad):
    entidad = Entidad.objects.get(id_entidad=id_entidad)
    entidad_form = EntidadForm(instance=entidad)
    
    if request.method == 'POST':
        entidad_form = EntidadForm(request.POST, instance = entidad)
        if entidad_form.is_valid():
            entidad_form.save()
            return redirect('list_entidad')
    return render(request, 'Entidad/edit_entidad.html',{'entidad_form': entidad_form})

    #DELETE entidad
def del_entidad(request, id_entidad):
    entidad_to_delete = Entidad.objects.get(pk = id_entidad)
    entidad_to_delete.delete()
    
    return redirect('list_entidad')


#==========================================> Expediente <============================================#
def expediente_pc(request, id_pc):
    # Obtener el PC principal con todas sus relaciones
    pc = get_object_or_404(Pc.objects.select_related(
        'id_chasis',
        'id_entidad'
    ).prefetch_related(
        'perifericos_set',
        'incidencias_set'
    ), id_pc=id_pc)
    
    # Obtener todos los componentes relacionados
    context = {'pc': pc}
    
    try:
        # Componentes directos
        context['chasis'] = pc.id_chasis
        context['placa_base'] = Placa_Base.objects.get(id_chasis=context['chasis'])
        context['procesador'] = Procesador.objects.get(id_placa=context['placa_base'])
        context['rams'] = Ram.objects.filter(id_placa=context['placa_base'])
        context['tarjetas_red'] = Tarjeta_Red.objects.filter(id_placa=context['placa_base'])
        
        # Componentes del chasis
        context['almacenamientos'] = Almacenamiento.objects.filter(id_chasis=context['chasis'])
        context['ranuras'] = Ranura_Expansion.objects.filter(id_chasis=context['chasis'])
        context['fuente'] = Fuente.objects.get(id_chasis=context['chasis'])
        context['lector'] = Lector.objects.get(id_chasis=context['chasis'])
        
        # Componentes adicionales
        context['perifericos'] = pc.perifericos_set.all()
        
    except ObjectDoesNotExist as e:
        context['error'] = f"Componente faltante: {str(e)}"
    
    return render(request, 'Expediente/expediente_pc.html', context)
def list_Ueb_exp(request): 
    # Obtener todas las entidades de tipo UEB
    uebs_exp = Entidad.objects.filter(tipoEntidad='UEB')
    
    # Crear un diccionario para almacenar las PCs por cada UEB
    entidad_with_pcs = {}
    
    for ent in uebs_exp:
        # Obtener las PCs asociadas a cada UEB
        pcs = Pc.objects.filter(id_entidad=ent)
        contad = pcs.count()
        entidad_with_pcs[ent] = contad
    
    context = {
        'entidad_with_pcs': entidad_with_pcs,
    }
    return render(request, 'Expediente/list_expedientes.html', context)
def list_Complejo_exp(request): 
    # Obtener todas las entidades de tipo UEB
    complejo_exp = Entidad.objects.filter(tipoEntidad='Complejo')
    
    # Crear un diccionario para almacenar las PCs por cada UEB
    entidad_with_pcs = {}
    
    for ent in complejo_exp:
        # Obtener las PCs asociadas a cada UEB
        pcs = Pc.objects.filter(id_entidad=ent)
        contad = pcs.count()
        entidad_with_pcs[ent] = contad
    
    context = {
        'entidad_with_pcs': entidad_with_pcs,
    }
    return render(request, 'Expediente/list_expedientes.html', context)
def list_Otros_exp(request): 
    # Obtener todas las entidades de tipo UEB
    otros_exp = Entidad.objects.filter(tipoEntidad='Otros')
    
    # Crear un diccionario para almacenar las PCs por cada UEB
    entidad_with_pcs = {}
    
    for ent in otros_exp:
        # Obtener las PCs asociadas a cada UEB
        pcs = Pc.objects.filter(id_entidad=ent)
        contad = pcs.count()
        entidad_with_pcs[ent] = contad
    
    context = {
        'entidad_with_pcs': entidad_with_pcs,
    }
    return render(request, 'Expediente/list_expedientes.html', context)
def lista_exp_por_nomb(request, id_entidad): 
    
    entidad = Entidad.objects.filter(id_entidad=id_entidad)    
    # Filtrar las PCs asociadas a la entidad
    pcs = Pc.objects.filter(id_entidad=id_entidad)
    
    context = {
        'entidad': entidad[0],
        'pcs': pcs,
    }
    
    return render(request, 'Expediente/exp_x_pcs.html', context)


#==========================================> Properties <============================================#


#==========================================> Properties <============================================#