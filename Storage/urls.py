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
    
    #===================== urls next ===================#
    
]