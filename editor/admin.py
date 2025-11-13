from django.contrib import admin
from .models import Map, Dienst, Attribut, Geopaeckli, App, Thema, Ebene, Tag, Wertetabelle, View, Workflow, Trigger


class MapAdmin(admin.ModelAdmin):
    # creates a nicer interface for the layer selection.
    filter_horizontal = ['dienste']

class DienstAdmin(admin.ModelAdmin):
    filter_horizontal = ['wertetabellen']
    list_display = ('technischer_name_dienst', 'name_dienst_de')

class GeopaeckliAdmin(admin.ModelAdmin):
    list_display = ('name_de', 'technischer_name')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name_de',)
    ordering = ('name_de',)
    search_fields = ('name_de',)

class ViewAdmin(admin.ModelAdmin):
    list_display = ('name_view', 'dienst')

class WorkflowAdmin(admin.ModelAdmin):
    filter_horizontal = ['apps']

class AttributInline(admin.StackedInline):
    model = Attribut
    extra = 0

class EbeneAdmin(admin.ModelAdmin):
    inlines = [AttributInline]
    filter_horizontal = ['tags', 'views']
    list_display = ('name', 'geopaeckli')

class WertetabelleAdmin(admin.ModelAdmin):
    list_display = ('name_tabelle', 'ebene')

class AttributAdmin(admin.ModelAdmin):
    list_display = ('name_attribut', 'ebene', 'wertetabelle')


# Register your models here.
admin.site.register(Map, MapAdmin)
admin.site.register(Dienst, DienstAdmin)
admin.site.register(Attribut, AttributAdmin)
admin.site.register(Geopaeckli, GeopaeckliAdmin)
admin.site.register(App)
admin.site.register(Thema)
admin.site.register(Ebene, EbeneAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Wertetabelle, WertetabelleAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(Trigger)


