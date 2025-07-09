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
    foerderprogramm = models.CharField(max_length=100)
    dokumentation = models.URLField(blank=True, null=True)
    bemerkungen = models.TextField(blank=True, null=True)
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE)

    def __str__(self):
        return self.titel_de
    
    class Meta:
        verbose_name = "Ebene"
        verbose_name_plural = "Ebenen"
        ordering = ["titel_de"]