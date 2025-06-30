from django.db import models

class App(models.Model):
    name_map_de = models.CharField(max_length=255)
    name_map_fr = models.CharField(max_length=255)
    zusammenfassung_de = models.TextField()
    zusammenfassung_fr = models.TextField()
    map = models.OneToOneField("Map", on_delete=models.CASCADE, related_name="app")

    def __str__(self):
        return self.name_map_de
   