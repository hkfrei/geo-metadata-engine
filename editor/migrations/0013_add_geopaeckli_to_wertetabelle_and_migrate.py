from django.db import migrations


class Migration(migrations.Migration):
    """Placeholder migration to satisfy Django migration loader.

    The original file was empty which raised BadMigrationError: no Migration class.
    This placeholder has no operations. Restore the original migration content from
    version control if you need the real schema/data changes applied here.
    """

    dependencies = [
        ("editor", "0012_remove_ebene_from_attribut"),
    ]

    operations = []
