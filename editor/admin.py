from django.contrib import admin
from django import forms
from .models import Map, Dienst, Attribut, Geopaeckli, App, Thema, Ebene, Tag, Wertetabelle, View, Workflow, Trigger
from django.db import models


class EbeneForm(forms.ModelForm):
    class Meta:
        model = Ebene
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Try to determine geopaeckli from POST/initial/instance to limit the
        # attributes_shared queryset on the form (helps during create).
        geop = None
        if self.data.get('geopaeckli'):
            try:
                geop = int(self.data.get('geopaeckli'))
            except Exception:
                geop = None
        elif self.initial.get('geopaeckli'):
            geop = self.initial.get('geopaeckli')
        elif self.instance and getattr(self.instance, 'geopaeckli', None):
            geop = getattr(self.instance.geopaeckli, 'id', None)

        if geop:
            # include attributes directly assigned to the Geopaeckli
            self.fields['attributes_shared'].queryset = Attribut.objects.filter(
                geopaeckli_id=geop
            )
            # and limit wertetabelle choices to same geopaeckli
            if 'wertetabelle' in self.fields:
                self.fields['wertetabelle'].queryset = Wertetabelle.objects.filter(geopaeckli_id=geop)

    def clean(self):
        cleaned = super().clean()
        attrs = cleaned.get('attributes_shared')
        geop = cleaned.get('geopaeckli')
        if attrs and geop:
            for attr in attrs:
                if getattr(attr, 'geopaeckli', None) != geop:
                    raise forms.ValidationError({'attributes_shared': "Ausgewählte Attribute müssen zum selben Geopäckli gehören wie die Ebene."})
        # Make the selected attributes available to the model.clean() via cache
        if attrs is not None:
            self.instance._attributes_shared_cache = list(attrs)
        return cleaned


class MapAdmin(admin.ModelAdmin):
    # creates a nicer interface for the layer selection.
    filter_horizontal = ['dienste']

class DienstAdmin(admin.ModelAdmin):
    filter_horizontal = ['wertetabellen']
    list_display = ('technischer_name_dienst', 'name_dienst_de')

class AttributInline(admin.StackedInline):
    model = Attribut
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit the wertetabelle choices to those belonging to the same geopaeckli
        # as the parent Geopaeckli when editing/adding inline under a Geopaeckli.
        if db_field.name == 'wertetabelle':
            geop = None
            # try POST/initial data first
            if request.POST.get('geopaeckli'):
                try:
                    geop = int(request.POST.get('geopaeckli'))
                except Exception:
                    geop = None
            # try to infer parent id from URL (/admin/editor/geopaeckli/<id>/change/)
            if not geop:
                try:
                    parts = request.path.strip('/').split('/')
                    if 'change' in parts:
                        idx = parts.index('change')
                        geop = int(parts[idx-1])
                except Exception:
                    geop = None
            if geop:
                kwargs['queryset'] = Wertetabelle.objects.filter(geopaeckli_id=geop)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Use raw_id_fields to allow fast lookup/search of Wertetabelle via popup
    raw_id_fields = ('wertetabelle',)

class GeopaeckliAdmin(admin.ModelAdmin):
    inlines = [AttributInline]
    list_display = ('name_de', 'technischer_name')
    prepopulated_fields = {'technischer_name': ('name_de',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ('name_de',)
    ordering = ('name_de',)
    search_fields = ('name_de',)

class ViewAdmin(admin.ModelAdmin):
    list_display = ('name_view', 'dienst')

class WorkflowAdmin(admin.ModelAdmin):
    filter_horizontal = ['apps']

class EbeneAdmin(admin.ModelAdmin):
    form = EbeneForm
    # show attributes_shared with the same UI as tags (horizontal filter)
    # Attributes are managed on the Geopaeckli level; remove inline here.
    filter_horizontal = ['tags', 'attributes_shared']
    list_display = ('name', 'geopaeckli')
    exclude = ('triggers', 'dienst', 'views')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'attributes_shared':
            # Try to get geopaeckli id from request path (/admin/editor/ebene/<id>/change/)
            try:
                parts = request.path.strip('/').split('/')
                if 'change' in parts:
                    idx = parts.index('change')
                    pk = int(parts[idx-1])
                    from .models import Ebene, Attribut
                    ebene = Ebene.objects.filter(pk=pk).first()
                    if ebene:
                        kwargs['queryset'] = Attribut.objects.filter(geopaeckli=ebene.geopaeckli)
            except Exception:
                pass
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Remove previous GeopaeckliAdmin definition further above

class WertetabelleAdmin(admin.ModelAdmin):
    list_display = ('name_tabelle', 'geopaeckli')
    # Hide the 'ebene' field in the admin form — use geopaeckli only in the editor
    exclude = ('ebene',)
    # enable searching in the popup/raw-id selector
    search_fields = ('name_tabelle',)

class AttributAdmin(admin.ModelAdmin):
    list_display = ('name_attribut', 'geopaeckli', 'wertetabelle')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit wertetabelle choices to Wertetabellen of the same geopaeckli as
        # the attribute being edited/created. Try POST, then object instance.
        if db_field.name == 'wertetabelle':
            geop = None
            if request.POST.get('geopaeckli'):
                try:
                    geop = int(request.POST.get('geopaeckli'))
                except Exception:
                    geop = None
            # if editing an existing object, try to get its geopaeckli
            if not geop:
                try:
                    parts = request.path.strip('/').split('/')
                    if 'change' in parts:
                        pk = int(parts[parts.index('change') - 1])
                        obj = Attribut.objects.filter(pk=pk).first()
                        if obj and obj.geopaeckli_id:
                            geop = obj.geopaeckli_id
                except Exception:
                    geop = None
            if geop:
                kwargs['queryset'] = Wertetabelle.objects.filter(geopaeckli_id=geop)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    # allow raw id popup search for wertetabelle
    raw_id_fields = ('wertetabelle',)


# Register your models here.
admin.site.register(Attribut, AttributAdmin)
admin.site.register(Geopaeckli, GeopaeckliAdmin)
admin.site.register(Thema)
admin.site.register(Ebene, EbeneAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Wertetabelle, WertetabelleAdmin)
# Note: Map, Dienst, App, View, Workflow and Trigger are intentionally not registered to hide them from the admin frontend.


