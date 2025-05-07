from django.db import models

class Webmap(models.Model):
    language_choices = [("DE", "Deutsch"), ("FR", "Französisch")]
    title = models.CharField("Name", max_length=200)
    description = models.TextField("Beschrieb")
    snippet = models.TextField("Snippet (kurze Zusammenfassung)")
    culture = models.CharField(
        "Sprache", max_length=2, choices=language_choices, default="DE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "_" + self.culture
