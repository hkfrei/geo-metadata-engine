from django.db import models
from django.utils.text import slugify


class Geopaeckli(models.Model):
    INTERVALL_CHOICES = [
        ('täglich', 'täglich'),
        ('wöchentlich', 'wöchentlich'),
        ('monatlich', 'monatlich'),
        ('quartalsweise', 'quartalsweise'),
        ('jährlich', 'jährlich'),
        ('bei Bedarf', 'bei Bedarf'),
        ('nie', 'nie'),
    ]

    name_de = models.CharField(max_length=200, default="Unbenannt")
    name_fr = models.CharField(max_length=200, default="Non nommé")
    technischer_name = models.CharField(max_length=100, unique=True)
    nachfuehrungsintervall = models.CharField(
        max_length=20, choices=INTERVALL_CHOICES, default='bei Bedarf'
    )
    dataowner = models.CharField(max_length=200, default="Unbekannt")
    datasteward = models.CharField(max_length=200, default="Unbekannt")
    dateneditor = models.CharField(max_length=200, default="Unbekannt")
    thema = models.ForeignKey(
        "Thema", on_delete=models.CASCADE, related_name='geopaeckli', null=True
    )

    def __str__(self):
        return f"{self.name_de} ({self.technischer_name})"

    class Meta:
        verbose_name = "Geopäckli"
        verbose_name_plural = "Geopäckli"
        ordering = ["name_de"]

    def save(self, *args, **kwargs):
        # Technischen Namen automatisch normalisieren (slugify → Unterstriche)
        # und Eindeutigkeit durch Nummerierung sicherstellen
        base = slugify(self.technischer_name or self.name_de or '').replace('-', '_') or 'unnamed'
        max_len = self._meta.get_field('technischer_name').max_length
        name = base[:max_len]
        counter = 1
        while Geopaeckli.objects.filter(technischer_name=name).exclude(pk=self.pk).exists():
            suffix = f"_{counter}"
            name = f"{base[:max_len - len(suffix)]}{suffix}"
            counter += 1
        self.technischer_name = name
        super().save(*args, **kwargs)
