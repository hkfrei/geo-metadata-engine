
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("editor", "0009_ebene_attributes_shared"),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribut',
            name='ebene',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='attribute',
                to='editor.ebene',
            ),
        ),
    ]
