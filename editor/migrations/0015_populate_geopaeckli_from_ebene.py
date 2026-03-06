from django.db import migrations


def forwards_populate_geopaeckli(apps, schema_editor):
    Wertetabelle = apps.get_model('editor', 'Wertetabelle')
    Ebene = apps.get_model('editor', 'Ebene')
    qs = Wertetabelle.objects.filter(ebene__isnull=False, geopaeckli__isnull=True)
    for w in qs:
        try:
            e = Ebene.objects.get(pk=w.ebene_id)
            # copy geopaeckli from Ebene
            w.geopaeckli_id = e.geopaeckli_id
            w.save(update_fields=['geopaeckli_id'])
        except Exception:
            # skip problematic rows
            continue


class Migration(migrations.Migration):

    dependencies = [
        ("editor", "0012_remove_ebene_from_attribut"),
    ]

    operations = [
        migrations.RunPython(forwards_populate_geopaeckli, migrations.RunPython.noop),
    ]
