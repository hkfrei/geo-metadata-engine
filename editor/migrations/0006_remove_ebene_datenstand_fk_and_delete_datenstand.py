from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0005_add_ebene_datenstand_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebene',
            name='datenstand',
        ),
        migrations.DeleteModel(
            name='Datenstand',
        ),
    ]
