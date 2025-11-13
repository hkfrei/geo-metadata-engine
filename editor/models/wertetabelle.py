from django.db import models

class Wertetabelle(models.Model):
    name_tabelle = models.CharField(max_length=255)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE, null=True, blank=True)
    ebene = models.ForeignKey("Ebene", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name_tabelle} ({self.ebene})"
    
    class Meta:
        verbose_name = "Wertetabelle"
        verbose_name_plural = "Wertetabellen"
        ordering = ["name_tabelle"]