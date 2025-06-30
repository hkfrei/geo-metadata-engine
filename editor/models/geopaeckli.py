from django.db import models

class Geopaeckli(models.Model):
    INTERVALL_CHOISES =[
                        ('täglich','täglich'),('wöchentlich','wöchentlich'),
                        ('monatlich','monatlich'),('quartalsweise','quartalsweise'),
                        ('jährlich','jährlich'),('bei Bedarf','bei Bedarf'),('nie','nie'), 
                    ]

    technischer_name = models.CharField(max_length=100, primary_key=True)
    name_de = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    nachfuehrungsintervall = models.CharField(max_length=20, choices=INTERVALL_CHOISES, blank=True, null=True)
    dataowner = models.CharField(max_length=100, blank=True, null=True)
    datasteward = models.CharField(max_length=100, blank=True, null=True)
    dateneditor = models.CharField(max_length=100, blank=True, null=True)
    

   # zeitstand = models.ForeignKey("Zeitstand", on_delete=models.CASCADE)
    datenstand = models.ForeignKey("Datenstand", on_delete=models.CASCADE)

    thema = models.ForeignKey("Thema", on_delete=models.CASCADE, related_name='geopaeckli')
    tags = models.ManyToManyField("Tag", related_name='geopaeckli', blank=True)
    # automatisierungen = models.ManyToManyField("Automatisierung", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_de