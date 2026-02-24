from django.db import models

class Wertetabelle(models.Model):
    name_tabelle = models.CharField(max_length=255)
    kurzbeschreibung_de = models.TextField()
    kurzbeschreibung_fr = models.TextField()
    # Use geopaeckli as primary FK in the model to match the current DB state.
    ebene = models.ForeignKey("Ebene", on_delete=models.CASCADE, null=True, blank=True)
    geopaeckli = models.ForeignKey("Geopaeckli", on_delete=models.CASCADE, null=True, blank=True, db_column='geopaeckli_id')

    def __str__(self):
        # Prefer ebene if present for display consistency.
        if getattr(self, 'ebene', None):
            return f"{self.name_tabelle} ({self.ebene})"
        return f"{self.name_tabelle} ({getattr(self, 'geopaeckli', None)})"
    
    class Meta:
        verbose_name = "Wertetabelle"
        verbose_name_plural = "Wertetabellen"
        ordering = ["name_tabelle"]