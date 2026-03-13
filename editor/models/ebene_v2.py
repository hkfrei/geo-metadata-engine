from django.db import models


class EbeneV2(models.Model):
    ZUGANGS_CHOICES = [
        ('A', 'öffentlich zugängliche Geodaten'),
        ('B', 'beschränkt öffentlich zugängliche Geodaten'),
        ('C', 'nicht öffentlich zugängliche Geodaten'),
    ]
    FEATUREKAT_CHOICES = [
        ('Raster', 'Raster'),
        ('Vektor', 'Vektor'),
        ('Tabelle', 'Tabelle'),
    ]
    FOERDERPROGRAMM_CHOICES = [
        ('NFA', 'NFA'),
        ('Kantonales Förderprogramm', 'Kantonales Förderprogramm'),
        ('ohne staatliche Förderung', 'ohne staatliche Förderung'),
        ('---', '---'),
    ]

    name = models.CharField(max_length=100)
    titel_de = models.CharField(max_length=200)
    titel_fr = models.CharField(max_length=200)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    editierbar = models.BooleanField()
    featurekategorie = models.CharField(max_length=50, choices=FEATUREKAT_CHOICES)
    zugangsberechtigung = models.CharField(max_length=1, choices=ZUGANGS_CHOICES)
    foerderprogramm = models.CharField(
        max_length=100, choices=FOERDERPROGRAMM_CHOICES, default='---'
    )
    dokumentation = models.TextField(blank=True, null=True)
    datenstand_date = models.DateField()
    geopaeckli = models.ForeignKey(
        "Geopaeckli", on_delete=models.CASCADE, related_name="v2_ebenen"
    )
    dienst = models.ForeignKey(
        "Dienst", on_delete=models.SET_NULL, null=True, blank=True, related_name="v2_ebenen"
    )
    tags = models.ManyToManyField("Tag", related_name="v2_ebenen", blank=True)
    triggers = models.ManyToManyField("Trigger", related_name="v2_ebenen", blank=True)
    views = models.ManyToManyField("View", related_name="v2_ebenen", blank=True)
    attribute = models.ManyToManyField(
        "AttributV2",
        related_name="v2_ebenen",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.geopaeckli})"

    class Meta:
        verbose_name = "Ebene V2"
        verbose_name_plural = "Ebenen V2"
        ordering = ["titel_de"]
