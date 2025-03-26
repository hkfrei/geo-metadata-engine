from django.contrib import admin
from .models import Layer, Layergroup

class LayergroupAdmin(admin.ModelAdmin):
    # creates a nicer interface for the layer selection.
    filter_horizontal = ['layer']

# Register your models here.
admin.site.register(Layer)
admin.site.register(Layergroup,LayergroupAdmin)