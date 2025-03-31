from django.urls import path
from . import views

app_name = "editor"
urlpatterns = [
    path("", views.index, name="index"),
    path("layers/", views.layers, name="layers"),
    path("layergroups/", views.layergroups, name="layergroups"),
    path("createwebmap/", views.create_webmap, name="createwebmap"),
    path("editwebmap/", views.edit_webmap, name="editwebmap"),
    path("updatewebmap/", views.update_webmap, name="updatewebmap"),
    path("updatewebmapsuccess/", views.update_webmap_success,
         name="updatewebmapsuccess"),
]
