from django.db import models

class View(models.Model):
    name_view = models.CharField(max_length=255)
    beschreibung_de = models.TextField()
    ebenen = models.ManyToManyField("Ebene", related_name="views")

    def __str__(self):
        return self.name_view