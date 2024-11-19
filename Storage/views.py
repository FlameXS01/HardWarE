from django.shortcuts import render,redirect
from Storage.form import*
from Storage.models import*

# Create your views here.

    #index view 
def index (request): 
    pc = Pc.objects.all()
    return render(request, 'base/index.html', {'pc': pc})

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
    chasis = Chasis.objects.all()
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
            #guardar el pc
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


#==========================================> NEW <============================================#