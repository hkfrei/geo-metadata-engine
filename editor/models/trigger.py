from django.db import models

class Trigger(models.Model):
    name = models.CharField(max_length=200,default="vollständiger Name")
    beschreibung_de = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Trigger"
        verbose_name_plural = "Trigger"
        ordering = ["name"]