from django.db import models

class Dienst(models.Model):
    technischer_name_dienst = models.CharField(max_length=255)
    name_dienst_de = models.CharField(max_length=255)
    name_dienst_fr = models.CharField(max_length=255)
    zusammenfassung_de = models.TextField()
    zusammenfassung_fr = models.TextField()
    quellennachweis_de = models.TextField()
    quellennachweis_fr = models.TextField()
    extern = models.BooleanField()
    owner = models.CharField(max_length=255)
    ebenen = models.ManyToManyField("Ebene", related_name="dienste")
    views = models.ManyToManyField("View", related_name="dienste")
    wertetabellen = models.ManyToManyField("Wertetabelle", related_name="dienste", blank=True)

    def __str__(self):
        return self.name_dienst_de
    
    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"
        ordering = ["name_dienst_de"]