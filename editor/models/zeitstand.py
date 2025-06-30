from django.db import models

class Zeitstand(models.Model):
    zeitstand = models.CharField(max_length=255)
    publikationsdatum = models.DateField()
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE, related_name="zeitstaende")

    def __str__(self):
        return f"{self.zeitstand} ({self.publikationsdatum})"