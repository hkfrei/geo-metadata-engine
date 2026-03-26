from django.db import models
from django.utils.text import slugify


class Thema(models.Model):
    technischer_name = models.CharField(max_length=200)
    beschreibung_de = models.TextField(blank=True)

    def __str__(self):
        return self.technischer_name

    def save(self, *args, **kwargs):
        base = slugify(self.technischer_name or '').replace('-', '_') or 'unnamed'
        max_len = self._meta.get_field('technischer_name').max_length
        name = base[:max_len]
        counter = 1
        while Thema.objects.filter(technischer_name=name).exclude(pk=self.pk).exists():
            suffix = f"_{counter}"
            name = f"{base[:max_len - len(suffix)]}{suffix}"
            counter += 1
        self.technischer_name = name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "Themen"
        ordering = ["technischer_name"]
