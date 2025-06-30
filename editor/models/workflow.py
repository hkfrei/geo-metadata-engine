from django.db import models
class Workflow(models.Model):
    name_workflow = models.CharField(max_length=255)
    beschreibung_de = models.TextField()
    apps = models.ManyToManyField("App", related_name="workflows")

    def __str__(self):
        return self.name_workflow