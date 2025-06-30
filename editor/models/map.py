from django.db import models
class Map(models.Model):
    name_map_de = models.CharField(max_length=255)
    name_map_fr = models.CharField(max_length=255)
    zusammenfassung_de = models.TextField()
    zusammenfassung_fr = models.TextField()
    dienste = models.ManyToManyField("Dienst", related_name="maps")

    def __str__(self):
        return f"{self.name_map_de} / {self.name_map_fr}"