from django.db import models

ATTRIBUTTYP_CHOICES = [
    ('int', 'Ganzzahl'),
    ('float', 'Gleitkommazahl'),
    ('date', 'Datum'),
    ('datetime', 'Datum mit Uhrzeit'),
    ('text', 'Text'),
    ('bool', 'Boolean'),
]


class AttributV2(models.Model):
    name_attribut = models.CharField(max_length=255)
    kurzbezeichnung_de = models.CharField(max_length=255)
    kurzbezeichnung_fr = models.CharField(max_length=255)
    beschreibung_de = models.TextField(blank=True, null=True)
    attributtyp = models.CharField(max_length=20, choices=ATTRIBUTTYP_CHOICES)
    attributlaenge = models.IntegerField()
    pflicht = models.BooleanField()
    unique = models.BooleanField()
    index = models.BooleanField()
    geopaeckli = models.ForeignKey(
        "Geopaeckli",
        on_delete=models.CASCADE,
        related_name="v2_attribute",
    )
    wertetabellen = models.ManyToManyField(
        "WertetabelleV2",
        related_name="v2_attribute",
        blank=True,
    )

    def __str__(self):
        return f"{self.name_attribut} ({self.geopaeckli})"

    class Meta:
        verbose_name = "Attribut V2"
        verbose_name_plural = "Attribute V2"
        ordering = ["name_attribut"]