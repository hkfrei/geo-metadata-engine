from django.db import models


class Wertetabelle(models.Model):
    name_tabelle = models.CharField(max_length=255)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    # Wertetabelle lebt am Geopäckli — unabhängig von Attributen und Ebenen
    geopaeckli = models.ForeignKey(
        "Geopaeckli",
        on_delete=models.CASCADE,
        related_name="wertetabellen",
    )

    def __str__(self):
        return f"{self.name_tabelle} ({self.geopaeckli})"

    class Meta:
        verbose_name = "Wertetabelle"
        verbose_name_plural = "Wertetabellen"
        ordering = ["name_tabelle"]
