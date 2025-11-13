from django.db import models
import datetime

class Zeitstand(models.Model):
    zeitstand = models.CharField(max_length=255, default="1.1.1900")
    publikationsdatum = models.DateField(default=datetime.date(1900, 1, 1))
    # geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE, related_name="zeitstaende")

    def __str__(self):
        return f"{self.zeitstand} ({self.publikationsdatum})"
    
    class Meta:
        verbose_name = "Zeitstand"
        verbose_name_plural = "Zeitstände"
        ordering = ["publikationsdatum"]