from django.db import models

class Wertetabelle(models.Model):
    name_tabelle = models.CharField(max_length=255)
    kurzbeschreibung_de = models.TextField()

    def __str__(self):
        return self.name_tabelle