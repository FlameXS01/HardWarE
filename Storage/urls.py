from django.urls import path
from Storage.views import * 

urlpatterns = [
    
    #INDEX
    path('', index , name="index"),
    
    #===================== urls pc ===================#
    
    path('pc/', list_pc , name="list_pc"),
    path('add_pc/',  add_pc ,name="add_pc"),
    path('edit_pc/<int:id_pc>', edit_pc, name="edit_pc"),
    path('del_pc/<int:id_pc>', del_pc, name="del_pc"), 
    
    #===================== urls chasis ===================#
    
    path('chasis/', list_chasis , name="list_chasis"),
    path('add_chasis/',  add_chasis ,name="add_chasis"),
    path('edit_chasis/<int:id_chasis>', edit_chasis, name="edit_chasis"),
    path('del_chasis/<int:id_chasis>', del_chasis, name="del_chasis"), 
    
    #===================== urls incidencia ===================#
    
    path('incidencia/', list_incidencia , name="list_incidencia"),
    path('add_incidencia/',  add_incidencia ,name="add_incidencia"),
    path('edit_incidencia/<int:id_incidencia>', edit_incidencia, name="edit_incidencia"),
    path('del_incidencia/<int:id_incidencia>', del_incidencia, name="del_incidencia"), 
    
    #===================== urls periferico ===================#
    
    path('periferico/', list_periferico , name="list_periferico"),
    path('add_periferico/',  add_periferico ,name="add_periferico"),
    path('edit_periferico/<int:id_periferico>', edit_periferico, name="edit_periferico"),
    path('del_periferico/<int:id_periferico>', del_periferico, name="del_periferico"), 
    
    #===================== urls fuente ===================#
    
    path('fuente/', list_fuente , name="list_fuente"),
    path('add_fuente/',  add_fuente ,name="add_fuente"),
    path('edit_fuente/<int:id_fuente>', edit_fuente, name="edit_fuente"),
    path('del_fuente/<int:id_fuente>', del_fuente, name="del_fuente"), 
    
    #===================== urls almacenamiento ===================#
    
    path('almacenamiento/', list_almacenamiento , name="list_almacenamiento"),
    path('add_almacenamiento/',  add_almacenamiento ,name="add_almacenamiento"),
    path('edit_almacenamiento/<int:id_almacenamiento>', edit_almacenamiento, name="edit_almacenamiento"),
    path('del_almacenamiento/<int:id_almacenamiento>', del_almacenamiento, name="del_almacenamiento"), 
    
    #===================== urls procesador ===================#
    
    path('procesador/', list_procesador , name="list_procesador"),
    path('add_procesador/',  add_procesador ,name="add_procesador"),
    path('edit_procesador/<int:id_procesador>', edit_procesador, name="edit_procesador"),
    path('del_procesador/<int:id_procesador>', del_procesador, name="del_procesador"), 
    
    #===================== urls motherb ===================#
    
    path('placa/', list_placa , name="list_placa"),
    path('add_placa/',  add_placa ,name="add_placa"),
    path('edit_placa/<int:id_placa>', edit_placa, name="edit_placa"),
    path('del_placa/<int:id_placa>', del_placa, name="del_placa"), 
    
    #===================== urls ram ===================#
    
    path('ram/', list_ram , name="list_ram"),
    path('add_ram/',  add_ram ,name="add_ram"),
    path('edit_ram/<int:id_ram>', edit_ram, name="edit_ram"),
    path('del_ram/<int:id_ram>', del_ram, name="del_ram"), 
    
    #===================== urls lector ===================#
    
    path('lector/', list_lector , name="list_lector"),
    path('add_lector/',  add_lector ,name="add_lector"),
    path('edit_lector/<int:id_lector>', edit_lector, name="edit_lector"),
    path('del_lector/<int:id_lector>', del_lector, name="del_lector"), 
    
    #===================== urls ranura ===================#
    
    path('ranura/', list_ranura , name="list_ranura"),
    path('add_ranura/',  add_ranura ,name="add_ranura"),
    path('edit_ranura/<int:id_ranura>', edit_ranura, name="edit_ranura"),
    path('del_ranura/<int:id_ranura>', del_ranura, name="del_ranura"), 
    
    #===================== urls next ===================#
    
    path('tarjeta/', list_tarjeta , name="list_tarjeta"),
    path('add_tarjeta/',  add_tarjeta ,name="add_tarjeta"),
    path('edit_tarjeta/<int:id_tarjeta>', edit_tarjeta, name="edit_tarjeta"),
    path('del_tarjeta/<int:id_tarjeta>', del_tarjeta, name="del_tarjeta"), 
    
    #===================== urls next ===================#
    
    path('prueba/',  registe ,name="prueba"),
]