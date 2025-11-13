from django.db import models


class Tag(models.Model):
    name_de = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)



    def __str__(self):
        return self.name_de