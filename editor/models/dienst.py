from django.db import models

OWNER_CHOICES = [
    ('awn', 'AWN'),
    ('agi', 'AGI'),
]


class Dienst(models.Model):
    technischer_name_dienst = models.CharField(max_length=255)
    name_dienst_de = models.CharField(max_length=255)
    name_dienst_fr = models.CharField(max_length=255)
    zusammenfassung_de = models.TextField()
    zusammenfassung_fr = models.TextField()
    quellennachweis_de = models.TextField()
    quellennachweis_fr = models.TextField()
    extern = models.BooleanField()
    owner = models.CharField(max_length=50, choices=OWNER_CHOICES)
    # Beziehung zu Wertetabelle im Konzept noch offen ("?") — weggelassen bis geklärt

    def __str__(self):
        return f"{self.technischer_name_dienst} ({self.name_dienst_de})"

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"
        ordering = ["name_dienst_de"]
