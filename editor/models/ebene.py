from django.db import models

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
                        ('Prosam','Prosam'),
                        ('Andere','Andere')
                        ]
    foerderprogramm = models.CharField(max_length=100, choices=FOERDERPROGRAMM_CHOISES, default='Andere')
    dokumentation = models.TextField(blank=True, null=True)
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE)
    # datenstand was a separate model; replace with an optional DateField on Ebene
    datenstand_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name='Ebene', blank=True)
    triggers = models.ManyToManyField("Trigger", related_name="ebenen", blank=True)
    dienst = models.ForeignKey("Dienst", on_delete=models.CASCADE, null=True, blank=True)
    views = models.ManyToManyField("View", blank=True)

    def __str__(self):
        return f"{self.name} ({self.geopaeckli})"
    
    class Meta:
        verbose_name = "Ebene"
        verbose_name_plural = "Ebenen"
        ordering = ["titel_de"]