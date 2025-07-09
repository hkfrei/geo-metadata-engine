from django.contrib import admin
from .models import Map, Dienst, Attribut, Datenstand, Geopaeckli, App, Thema, Ebene, Tag, Wertetabelle, View, Workflow, Zeitstand


class MapAdmin(admin.ModelAdmin):
    # creates a nicer interface for the layer selection.
    filter_horizontal = ['dienste']

class DienstAdmin(admin.ModelAdmin):
    filter_horizontal = ['ebenen', 'views', 'wertetabellen']

class GeopaeckliAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']

class TagAdmin(admin.ModelAdmin):
    filter_horizontal = ['ebenen']

class ViewAdmin(admin.ModelAdmin):
    filter_horizontal = ['ebenen']

class WorkflowAdmin(admin.ModelAdmin):
    filter_horizontal = ['apps']

# Register your models here.
admin.site.register(Map, MapAdmin)
admin.site.register(Dienst, DienstAdmin)
admin.site.register(Attribut)
admin.site.register(Datenstand)
admin.site.register(Geopaeckli, GeopaeckliAdmin)
admin.site.register(App)
admin.site.register(Thema)
admin.site.register(Ebene)
admin.site.register(Tag, TagAdmin)
admin.site.register(Wertetabelle)
admin.site.register(View, ViewAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(Zeitstand)

