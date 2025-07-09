from django.db import models


class Thema(models.Model):
    technischer_name = models.CharField(max_length=200)
    beschreibung_de = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.technischer_name
    
    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "Themen"
        ordering = ["technischer_name"]