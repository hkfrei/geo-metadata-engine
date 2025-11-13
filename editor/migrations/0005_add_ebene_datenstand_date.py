from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_remove_ebene_bemerkungen'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebene',
            name='datenstand_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
