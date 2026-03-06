from django.db import models
from django.core.exceptions import ValidationError

class Ebene(models.Model):
    ZUGANGS_CHOISES = [
                        ('A','öffentlich zugängliche Geodaten'),
                        ('B','beschränkt öffentlich zugängliche Geodaten'),
                        ('C','nicht öffentlich zugängliche Geodaten')
                        ]
    FEATUREKAT_CHOISES = [
                        ('Raster','Raster'),
                        ('Vektor','Vektor'),
                        ('Tabelle','Tabelle')
                        ]
    name = models.CharField(max_length=100)
    titel_de = models.CharField(max_length=200)
    titel_fr = models.CharField(max_length=200)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    editierbar = models.BooleanField()
    featurekategorie = models.CharField(max_length=50,choices= FEATUREKAT_CHOISES)
    zugangsberechtigung = models.CharField(max_length=1, choices = ZUGANGS_CHOISES)
    FOERDERPROGRAMM_CHOISES = [
                        ('NFA','NFA'),
                        ('Kantonales Förderprogramm','Kantonales Förderprogramm'),
                        ('ohne staatliche Förderung','ohne staatliche Förderung'),
                        ('---','---')
                        ]
    foerderprogramm = models.CharField(max_length=100, choices=FOERDERPROGRAMM_CHOISES, default='---')
    dokumentation = models.TextField(blank=True, null=True)
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE)
    # datenstand was a separate model; replace with an optional DateField on Ebene
    datenstand_date = models.DateField(null=False, blank=False)
    tags = models.ManyToManyField("Tag", related_name='Ebene', blank=True)
    triggers = models.ManyToManyField("Trigger", related_name="ebenen", blank=True)
    dienst = models.ForeignKey("Dienst", on_delete=models.CASCADE, null=True, blank=True)
    views = models.ManyToManyField("View", blank=True)

    # Many-to-many to allow selecting existing Attribut objects for this Ebene
    attributes_shared = models.ManyToManyField("Attribut", blank=True, related_name="shared_in_ebenen")

    def clean(self):
        super().clean()
        # Ensure any selected shared attributes belong to the same Geopaeckli as this Ebene
        if not self.geopaeckli:
            return
        # If instance is not yet saved (no pk), attributes_shared may be set via
        # a form. We attempt to access the m2m through _attributes_shared_cache
        # if available, otherwise fall back to the related manager (works for
        # saved instances).
        attrs = []
        try:
            # When a ModelForm is used, Django sets an _attributes_shared_cache
            attrs = list(getattr(self, '_attributes_shared_cache', []))
        except Exception:
            attrs = []

        if not attrs and self.pk is not None:
            attrs = list(self.attributes_shared.all())

        for attr in attrs:
            # Attribut may not have an 'ebene' field (DB/schema may use geopaeckli
            # on Attribut). Use getattr to avoid AttributeError and fall back to
            # comparing the geopaeckli relation if available.
            attr_ebene = getattr(attr, 'ebene', None)
            attr_geop = getattr(attr, 'geopaeckli', None)
            if attr_ebene and getattr(attr_ebene, 'geopaeckli', None) != self.geopaeckli:
                raise ValidationError({
                    'attributes_shared': "Ausgewählte Attribute müssen zum selben Geopäckli gehören wie die Ebene."
                })
            if not attr_ebene and attr_geop and attr_geop != self.geopaeckli:
                raise ValidationError({
                    'attributes_shared': "Ausgewählte Attribute müssen zum selben Geopäckli gehören wie die Ebene."
                })

    def attributes_shared_qs_for_geopaeckli(self):
        """Helper: return queryset of attributes belonging to this Ebene's Geopaeckli.
        Useful for admin/form filtering.
        """
        from .attribut import Attribut
        if not self.geopaeckli:
            return Attribut.objects.none()
        # Attribut may be linked directly to a Geopaeckli (geopaeckli field)
        # or via an ebene FK. Prefer direct geopaeckli relation if present.
        return Attribut.objects.filter(models.Q(geopaeckli=self.geopaeckli) | models.Q(ebene__geopaeckli=self.geopaeckli))

    def __str__(self):
        return f"{self.name} ({self.geopaeckli})"
    
    class Meta:
        verbose_name = "Ebene"
        verbose_name_plural = "Ebenen"
        ordering = ["titel_de"]