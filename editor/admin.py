from django.contrib import admin
from django import forms
from .models import (
    Thema, Geopaeckli, Ebene, Attribut, Wertetabelle,
    Dienst, View, Tag, Trigger,
    # Map, App, Workflow — models bleiben erhalten, vorerst nicht registriert
)


# ---------------------------------------------------------------------------
# Wertetabelle Inline — erscheint unter Attribut
# ---------------------------------------------------------------------------
class WertetabelleInline(admin.TabularInline):
    model = Attribut.wertetabellen.through
    extra = 0
    verbose_name = "Wertetabelle"
    verbose_name_plural = "Wertetabellen"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'wertetabelle':
            geop_id = _geopaeckli_id_from_request(request, 'attribut')
            if geop_id:
                kwargs['queryset'] = Wertetabelle.objects.filter(geopaeckli_id=geop_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ---------------------------------------------------------------------------
# Attribut Inline — erscheint unter Geopäckli
# ---------------------------------------------------------------------------
class AttributInline(admin.StackedInline):
    model = Attribut
    extra = 0
    show_change_link = True
    fields = (
        'name_attribut', 'kurzbezeichnung_de', 'kurzbezeichnung_fr',
        'beschreibung_de', 'attributtyp', 'attributlaenge',
        'pflicht', 'unique', 'index',
    )


# ---------------------------------------------------------------------------
# Hilfsfunktion: Geopäckli-ID aus Request-Pfad lesen
# ---------------------------------------------------------------------------
def _geopaeckli_id_from_request(request, model_name):
    try:
        parts = request.path.strip('/').split('/')
        if 'change' in parts:
            pk = int(parts[parts.index('change') - 1])
            if model_name == 'attribut':
                obj = Attribut.objects.filter(pk=pk).first()
                return obj.geopaeckli_id if obj else None
            if model_name == 'ebene':
                obj = Ebene.objects.filter(pk=pk).first()
                return obj.geopaeckli_id if obj else None
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Ebene Form — filtert Attribut-Auswahl auf dasselbe Geopäckli
# ---------------------------------------------------------------------------
class EbeneForm(forms.ModelForm):
    class Meta:
        model = Ebene
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
            self.fields['attribute'].queryset = Attribut.objects.filter(
                geopaeckli_id=geop_id
            )
        else:
            self.fields['attribute'].queryset = Attribut.objects.none()

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


# ---------------------------------------------------------------------------
# Ebene
# ---------------------------------------------------------------------------
class EbeneAdmin(admin.ModelAdmin):
    form = EbeneForm
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
        ('Tags', {
            'fields': ('tags',),
        }),
        ('Weitere Verknüpfungen', {
            'classes': ('collapse',),
            'fields': ('triggers', 'views'),
        }),
    )


# ---------------------------------------------------------------------------
# Attribut — mit Wertetabellen-Inline
# ---------------------------------------------------------------------------
class AttributAdmin(admin.ModelAdmin):
    inlines = [WertetabelleInline]
    list_display = ('name_attribut', 'geopaeckli', 'attributtyp', 'anzahl_wertetabellen')
    list_filter = ('geopaeckli', 'attributtyp')
    search_fields = ('name_attribut',)

    def anzahl_wertetabellen(self, obj):
        return obj.wertetabellen.count()
    anzahl_wertetabellen.short_description = "# Wertetabellen"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'geopaeckli':
            kwargs['queryset'] = Geopaeckli.objects.order_by('name_de')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ---------------------------------------------------------------------------
# Wertetabelle
# ---------------------------------------------------------------------------
class WertetabelleAdmin(admin.ModelAdmin):
    list_display = ('name_tabelle', 'geopaeckli', 'anzahl_attribute')
    list_filter = ('geopaeckli',)
    search_fields = ('name_tabelle',)

    def anzahl_attribute(self, obj):
        return obj.attribute.count()
    anzahl_attribute.short_description = "# Attribute"


# ---------------------------------------------------------------------------
# Geopäckli — Attribute als Inline
# ---------------------------------------------------------------------------
class GeopaeckliAdmin(admin.ModelAdmin):
    inlines = [AttributInline]
    list_display = ('name_de', 'technischer_name', 'thema')
    prepopulated_fields = {'technischer_name': ('name_de',)}
    search_fields = ('name_de', 'technischer_name')
    list_filter = ('thema',)


# ---------------------------------------------------------------------------
# Sonstige
# ---------------------------------------------------------------------------
class DienstAdmin(admin.ModelAdmin):
    list_display = ('technischer_name_dienst', 'name_dienst_de', 'owner')
    search_fields = ('technischer_name_dienst', 'name_dienst_de')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name_de', 'name_fr')
    search_fields = ('name_de',)


class ViewAdmin(admin.ModelAdmin):
    list_display = ('name_view', 'dienst')
    list_filter = ('dienst',)


# ---------------------------------------------------------------------------
# Registrierungen
# ---------------------------------------------------------------------------
admin.site.register(Thema)
admin.site.register(Geopaeckli, GeopaeckliAdmin)
admin.site.register(Ebene, EbeneAdmin)
admin.site.register(Attribut, AttributAdmin)
admin.site.register(Wertetabelle, WertetabelleAdmin)
admin.site.register(Dienst, DienstAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Trigger)
# Map, App, Workflow — vorerst nicht registriert