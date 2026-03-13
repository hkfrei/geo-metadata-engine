from django.contrib import admin
from django import forms
from django.db import models

from .models import (
    Map, Dienst, Attribut, Geopaeckli, App, Thema, Ebene,
    Tag, Wertetabelle, View, Workflow, Trigger,
    AttributV2, WertetabelleV2, EbeneV2,
)


# ===========================================================================
# ALTE MODELS (unverändert, ausser Registrierung unten auskommentiert)
# ===========================================================================

class EbeneForm(forms.ModelForm):
    class Meta:
        model = Ebene
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            self.fields['attributes_shared'].queryset = Attribut.objects.filter(
                geopaeckli_id=geop
            )
            if 'wertetabelle' in self.fields:
                self.fields['wertetabelle'].queryset = Wertetabelle.objects.filter(
                    geopaeckli_id=geop
                )

    def clean(self):
        cleaned = super().clean()
        attrs = cleaned.get('attributes_shared')
        geop = cleaned.get('geopaeckli')
        if attrs and geop:
            for attr in attrs:
                if getattr(attr, 'geopaeckli', None) != geop:
                    raise forms.ValidationError({
                        'attributes_shared': "Ausgewählte Attribute müssen zum selben Geopäckli gehören wie die Ebene."
                    })
        if attrs is not None:
            self.instance._attributes_shared_cache = list(attrs)
        return cleaned


class MapAdmin(admin.ModelAdmin):
    filter_horizontal = ['dienste']

class DienstAdmin(admin.ModelAdmin):
    filter_horizontal = ['wertetabellen']
    list_display = ('technischer_name_dienst', 'name_dienst_de')

class AttributInline(admin.StackedInline):
    model = Attribut
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'wertetabelle':
            geop = None
            if request.POST.get('geopaeckli'):
                try:
                    geop = int(request.POST.get('geopaeckli'))
                except Exception:
                    geop = None
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
    filter_horizontal = ['tags', 'attributes_shared']
    list_display = ('name', 'geopaeckli')
    exclude = ('triggers', 'dienst', 'views')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'attributes_shared':
            try:
                parts = request.path.strip('/').split('/')
                if 'change' in parts:
                    idx = parts.index('change')
                    pk = int(parts[idx-1])
                    ebene = Ebene.objects.filter(pk=pk).first()
                    if ebene:
                        kwargs['queryset'] = Attribut.objects.filter(geopaeckli=ebene.geopaeckli)
            except Exception:
                pass
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class WertetabelleAdmin(admin.ModelAdmin):
    list_display = ('name_tabelle', 'geopaeckli')
    exclude = ('ebene',)
    search_fields = ('name_tabelle',)

class AttributAdmin(admin.ModelAdmin):
    list_display = ('name_attribut', 'geopaeckli', 'wertetabelle')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'wertetabelle':
            geop = None
            if request.POST.get('geopaeckli'):
                try:
                    geop = int(request.POST.get('geopaeckli'))
                except Exception:
                    geop = None
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

    raw_id_fields = ('wertetabelle',)


# ===========================================================================
# V2 MODELS
# ===========================================================================

class WertetabelleV2Inline(admin.TabularInline):
    model = AttributV2.wertetabellen.through
    extra = 0
    verbose_name = "Wertetabelle V2"
    verbose_name_plural = "Wertetabellen V2"


class AttributV2Inline(admin.StackedInline):
    model = AttributV2
    extra = 0
    show_change_link = True
    fields = (
        'name_attribut', 'kurzbezeichnung_de', 'kurzbezeichnung_fr',
        'beschreibung_de', 'attributtyp', 'attributlaenge',
        'pflicht', 'unique', 'index',
    )


class EbeneV2Form(forms.ModelForm):
    class Meta:
        model = EbeneV2
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        geop_id = None
        if self.data.get('geopaeckli'):
            try:
                geop_id = int(self.data['geopaeckli'])
            except (ValueError, TypeError):
                pass
        if not geop_id and self.instance and self.instance.pk:
            geop_id = self.instance.geopaeckli_id

        if geop_id:
            self.fields['attribute'].queryset = AttributV2.objects.filter(
                geopaeckli_id=geop_id
            )
        else:
            self.fields['attribute'].queryset = AttributV2.objects.none()

    def clean(self):
        cleaned = super().clean()
        attribute = cleaned.get('attribute')
        geopaeckli = cleaned.get('geopaeckli')
        if attribute and geopaeckli:
            falsche = [a for a in attribute if a.geopaeckli != geopaeckli]
            if falsche:
                raise forms.ValidationError({
                    'attribute': (
                        "Folgende Attribute gehören nicht zum gewählten Geopäckli: "
                        + ", ".join(str(a) for a in falsche)
                    )
                })
        return cleaned


class EbeneV2Admin(admin.ModelAdmin):
    form = EbeneV2Form
    list_display = ('name', 'geopaeckli', 'dienst', 'featurekategorie')
    list_filter = ('geopaeckli', 'featurekategorie', 'zugangsberechtigung')
    search_fields = ('name', 'titel_de')
    filter_horizontal = ('attribute', 'tags', 'triggers', 'views')
    fieldsets = (
        (None, {
            'fields': (
                'name', 'titel_de', 'titel_fr',
                'kurzbeschreibung_de', 'kurzbeschreibung_fr',
                'featurekategorie', 'zugangsberechtigung', 'foerderprogramm',
                'editierbar', 'datenstand_date', 'dokumentation',
                'geopaeckli', 'dienst',
            ),
        }),
        ('Attribute', {
            'fields': ('attribute',),
            'description': 'Nur Attribute des gewählten Geopäcklis werden angezeigt.',
        }),
        ('Weitere Verknüpfungen', {
            'classes': ('collapse',),
            'fields': ('tags', 'triggers', 'views'),
        }),
    )


class AttributV2Admin(admin.ModelAdmin):
    inlines = [WertetabelleV2Inline]
    list_display = ('name_attribut', 'geopaeckli', 'attributtyp', 'anzahl_wertetabellen')
    list_filter = ('geopaeckli', 'attributtyp')
    search_fields = ('name_attribut',)

    def anzahl_wertetabellen(self, obj):
        return obj.wertetabellen.count()
    anzahl_wertetabellen.short_description = "# Wertetabellen"


class WertetabelleV2Admin(admin.ModelAdmin):
    list_display = ('name_tabelle', 'geopaeckli', 'anzahl_attribute')
    list_filter = ('geopaeckli',)
    search_fields = ('name_tabelle',)

    def anzahl_attribute(self, obj):
        return obj.v2_attribute.count()
    anzahl_attribute.short_description = "# Attribute"


class GeopaeckliV2Admin(admin.ModelAdmin):
    inlines = [AttributV2Inline]
    list_display = ('name_de', 'technischer_name', 'thema')
    prepopulated_fields = {'technischer_name': ('name_de',)}
    search_fields = ('name_de', 'technischer_name')
    list_filter = ('thema',)


# ===========================================================================
# REGISTRIERUNGEN
# Alte Models auskommentiert — V2 aktiv
# ===========================================================================

# admin.site.register(Attribut, AttributAdmin)
# admin.site.register(Wertetabelle, WertetabelleAdmin)
# admin.site.register(Ebene, EbeneAdmin)
# admin.site.register(Geopaeckli, GeopaeckliAdmin)

admin.site.register(Thema)
admin.site.register(Geopaeckli, GeopaeckliV2Admin)
admin.site.register(Tag, TagAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(AttributV2, AttributV2Admin)
admin.site.register(WertetabelleV2, WertetabelleV2Admin)
admin.site.register(EbeneV2, EbeneV2Admin)
