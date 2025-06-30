from django.contrib import admin
from .models import Layer, Layergroup, Webmap, Map, Dienst, Attribut, Datenstand, Geopaeckli, App, Thema, Ebene, Tag, Wertetabelle, View, Workflow, Zeitstand


class LayergroupAdmin(admin.ModelAdmin):
    # creates a nicer interface for the layer selection.
    filter_horizontal = ['layer']


# Register your models here.
admin.site.register(Layer)
admin.site.register(Webmap)
admin.site.register(Layergroup, LayergroupAdmin)
admin.site.register(Map)
admin.site.register(Dienst)
admin.site.register(Attribut)
admin.site.register(Datenstand)
admin.site.register(Geopaeckli)
admin.site.register(App)
admin.site.register(Thema)
admin.site.register(Ebene)
admin.site.register(Tag)
admin.site.register(Wertetabelle)
admin.site.register(View)
admin.site.register(Workflow)
admin.site.register(Zeitstand)

