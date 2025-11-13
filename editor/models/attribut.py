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
    ebene = models.ForeignKey("Ebene", on_delete=models.CASCADE, related_name="attribute", null=True, blank=True)
    wertetabelle = models.ForeignKey("Wertetabelle", on_delete=models.CASCADE, related_name="attribute", null=True, blank=True)

    def __str__(self):
        if self.ebene:
            return f"{self.name_attribut} ({self.ebene})"
        elif self.wertetabelle:
            return f"{self.name_attribut} ({self.wertetabelle})"
        return self.name_attribut

    class Meta:
        verbose_name = "Attribut"
        verbose_name_plural = "Attribute"
        ordering = ["name_attribut"]
        

    def clean(self):
        super().clean()
        # Attribut must be linked to an Ebene. Wertetabelle is optional and may
        # be provided in addition to the Ebene, but cannot be used as a replacement.
        if not self.ebene:
            raise ValidationError("Ein Attribut muss einer Ebene zugeordnet sein.")