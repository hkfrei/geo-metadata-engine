from django.db import models

class Attribut(models.Model):
    name_attribut = models.CharField(max_length=255)
    kurzbezeichnung_de = models.CharField(max_length=255)
    kurzbezeichnung_fr = models.CharField(max_length=255)
    beschreibung_de = models.TextField(blank=True, null=True)
    attributtyp = models.CharField(max_length=255)
    attributlaenge = models.IntegerField()
    pflicht = models.BooleanField()
    unique = models.BooleanField()
    index = models.BooleanField()
    ebene = models.ForeignKey("Ebene", on_delete=models.CASCADE, related_name="attribute", null=True, blank=True)
    wertetabelle = models.ForeignKey("Wertetabelle", on_delete=models.CASCADE, related_name="attribute", null=True, blank=True)
    
    def __str__(self):
        return self.name_attribut
    
    class Meta:
        verbose_name = "Attribut"
        verbose_name_plural = "Attribute"
        ordering = ["name_attribut"]