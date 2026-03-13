from django.db import models


class WertetabelleV2(models.Model):
    name_tabelle = models.CharField(max_length=255)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    geopaeckli = models.ForeignKey(
        "Geopaeckli",
        on_delete=models.CASCADE,
        related_name="v2_wertetabellen",
    )

    def __str__(self):
        return f"{self.name_tabelle} ({self.geopaeckli})"

    class Meta:
        verbose_name = "Wertetabelle V2"
        verbose_name_plural = "Wertetabellen V2"
        ordering = ["name_tabelle"]
