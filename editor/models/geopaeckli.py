from django.db import models

class Geopaeckli(models.Model):
    INTERVALL_CHOISES =[
                        ('täglich','täglich'),('wöchentlich','wöchentlich'),
                        ('monatlich','monatlich'),('quartalsweise','quartalsweise'),
                        ('jährlich','jährlich'),('bei Bedarf','bei Bedarf'),('nie','nie'), 
                    ]

    
    name_de = models.CharField(max_length=200, default="Unbenannt")
    name_fr = models.CharField(max_length=200, default="Non nommé")
    technischer_name = models.CharField(max_length=100, unique=True)
    nachfuehrungsintervall = models.CharField(max_length=20, choices=INTERVALL_CHOISES,default='bitte wählen')
    dataowner = models.CharField(max_length=200, default="Unbekannt")
    datasteward = models.CharField(max_length=200, default="Unbekannt")
    dateneditor = models.CharField(max_length=200, default="Unbekannt")
    

    # Zeitstand model removed; keep a text field to store previous zeitstand value if needed
    zeitstand_text = models.CharField(max_length=255, blank=True, null=True)
    # datenstand = models.ForeignKey("Datenstand", on_delete=models.CASCADE)

    thema = models.ForeignKey("Thema", on_delete=models.CASCADE, related_name='geopaeckli',null=True)
    # automatisierungen = models.ManyToManyField("Automatisierung", blank=True)

    

    def __str__(self):
        return f"{self.name_de} ({self.technischer_name})"
    
    class Meta:
        verbose_name = "Geopäckli"
        verbose_name_plural = "Geopäckli"
        ordering = ["name_de"]