from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify


class Thema(models.Model):
    technischer_name = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9_-]+$',
                message='Technischer Name darf keine Leerzeichen enthalten und nur Buchstaben, Zahlen, Unterstrich oder Bindestrich.'
            )
        ]
    )
    beschreibung_de = models.TextField(default="hier muss eine Beschreibung stehen")
    

    def __str__(self):
        return self.technischer_name
    
    def save(self, *args, **kwargs):
        # Normalisiere technischen Namen automatisch (slugify -> Unterstrich) und stelle Einzigartigkeit sicher
        base_source = self.technischer_name or ''
        base = slugify(base_source).replace('-', '_')
        if not base:
            base = 'unnamed'
        max_len = self._meta.get_field('technischer_name').max_length
        name = base[:max_len]
        counter = 1
        while Thema.objects.filter(technischer_name=name).exclude(pk=self.pk).exists():
            suffix = f"_{counter}"
            allowed = max_len - len(suffix)
            name = f"{base[:allowed]}{suffix}"
            counter += 1
        self.technischer_name = name
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Thema"
        verbose_name_plural = "Themen"
        ordering = ["technischer_name"]