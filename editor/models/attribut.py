from django.core.exceptions import ValidationError
from django.db import models

ATTRIBUTTYP_CHOICES = [
    ('int', 'Ganzzahl'),
    ('float', 'Gleitkommazahl'),
    ('date', 'Datum'),
    ('datetime', 'Datum mit Uhrzeit'),
    ('text', 'Text'),
    ('bool', 'Boolean'),
]

class Attribut(models.Model):
    name_attribut = models.CharField(max_length=255)
    kurzbezeichnung_de = models.CharField(max_length=255)
    kurzbezeichnung_fr = models.CharField(max_length=255)
    beschreibung_de = models.TextField(blank=True, null=True)
    attributtyp = models.CharField(max_length=20, choices=ATTRIBUTTYP_CHOICES)
    attributlaenge = models.IntegerField()
    pflicht = models.BooleanField()
    unique = models.BooleanField()
    index = models.BooleanField()
    # Use geopaeckli FK only (DB has geopaeckli_id; ebene_id is not present
    # in editor_attribut). This avoids missing-column errors in the admin.
    geopaeckli = models.ForeignKey(
        "Geopaeckli",
        on_delete=models.SET_NULL,
        related_name="attribute_geopaeckli",
        null=True,
        blank=True,
    )
    wertetabelle = models.ForeignKey("Wertetabelle", on_delete=models.CASCADE, related_name="attribute", null=True, blank=True)

    def __str__(self):
        if getattr(self, 'geopaeckli', None):
            return f"{self.name_attribut} ({self.geopaeckli})"
        elif self.wertetabelle:
            return f"{self.name_attribut} ({self.wertetabelle})"
        return self.name_attribut

    class Meta:
        verbose_name = "Attribut"
        verbose_name_plural = "Attribute"
        ordering = ["name_attribut"]
        

    def clean(self):
        super().clean()
        # Attributes may be unbound from an Ebene and belong to a Geopaeckli.
        # Keep validation light here; DB enforces relational integrity.
        return