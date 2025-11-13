from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geopaeckli',
            name='zeitstand',
        ),
        migrations.DeleteModel(
            name='Zeitstand',
        ),
    ]
