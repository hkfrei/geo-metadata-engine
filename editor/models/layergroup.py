from django.db import models

class Layergroup(models.Model):
    name = models.CharField(max_length=200)
    layer = models.ManyToManyField("Layer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

