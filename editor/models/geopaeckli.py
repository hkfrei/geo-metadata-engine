from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify

class Geopaeckli(models.Model):
    INTERVALL_CHOISES =[
                        ('täglich','täglich'),('wöchentlich','wöchentlich'),
                        ('monatlich','monatlich'),('quartalsweise','quartalsweise'),
                        ('jährlich','jährlich'),('bei Bedarf','bei Bedarf'),('nie','nie'), 
                    ]

    
    name_de = models.CharField(max_length=200, default="Unbenannt")
    name_fr = models.CharField(max_length=200, default="Non nommé")
    technischer_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9_-]+$',
                message='Technischer Name darf keine Leerzeichen enthalten und nur Buchstaben, Zahlen, Unterstrich oder Bindestrich.'
            )
        ]
    )
    nachfuehrungsintervall = models.CharField(max_length=20, choices=INTERVALL_CHOISES,default='bitte wählen')
    dataowner = models.CharField(max_length=200, default="Unbekannt")
    datasteward = models.CharField(max_length=200, default="Unbekannt")
    dateneditor = models.CharField(max_length=200, default="Unbekannt")
    

    # Zeitstand model removed; keep a text field to store previous zeitstand value if needed
    # zeitstand_text = models.CharField(max_length=255, blank=True, null=True)
    # datenstand = models.ForeignKey("Datenstand", on_delete=models.CASCADE)

    thema = models.ForeignKey("Thema", on_delete=models.CASCADE, related_name='geopaeckli',null=True)
    # automatisierungen = models.ManyToManyField("Automatisierung", blank=True)

    

    def __str__(self):
        return f"{self.name_de} ({self.technischer_name})"
    
    class Meta:
        verbose_name = "Geopäckli"
        verbose_name_plural = "Geopäckli"
        ordering = ["name_de"]

    def save(self, *args, **kwargs):
        # Normalisiere technischen Namen automatisch und stelle Einzigartigkeit sicher
        base_source = self.technischer_name or self.name_de or ''
        base = slugify(base_source).replace('-', '_')
        if not base:
            base = 'unnamed'
        # Kürze auf max Länge und iteriere bei Kollisionen
        max_len = self._meta.get_field('technischer_name').max_length
        name = base[:max_len]
        counter = 1
        while Geopaeckli.objects.filter(technischer_name=name).exclude(pk=self.pk).exists():
            suffix = f"_{counter}"
            allowed = max_len - len(suffix)
            name = f"{base[:allowed]}{suffix}"
            counter += 1
        self.technischer_name = name
        super().save(*args, **kwargs)