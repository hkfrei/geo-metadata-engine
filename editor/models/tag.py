from django.db import models


class Tag(models.Model):
    name_de = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ebenen = models.ManyToManyField("Ebene", blank=True)

    def __str__(self):
        return self.name_de