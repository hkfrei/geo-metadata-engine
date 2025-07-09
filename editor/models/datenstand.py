from django.db import models

class Datenstand(models.Model):
    datenstand = models.CharField(max_length=255)
    ebene = models.ForeignKey("Ebene", on_delete=models.CASCADE, related_name="datenstaende")

    def __str__(self):
        return self.datenstand
    
    class Meta:
        verbose_name = "Datenstand"
        verbose_name_plural = "Datenstände"
        ordering = ["datenstand"]