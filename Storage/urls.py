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
    
    #===================== next ===================#
    
]