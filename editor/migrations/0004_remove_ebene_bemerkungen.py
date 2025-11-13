from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_geopaeckli_zeitstand_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebene',
            name='bemerkungen',
        ),
    ]
