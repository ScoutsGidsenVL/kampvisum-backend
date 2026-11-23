from django.db import migrations


class Migration(migrations.Migration):
    """
    ScoutsGroup is identified by its groepsnummer (number) only: the internal GA id is no longer kept.

    ScoutsGroup is an unmanaged model (managed = False), so this only updates the migration state.
    """

    dependencies = [
        ("scouts_auth", "0006_remove_unused_groupadmin_fields"),
    ]

    operations = [
        migrations.RemoveField(model_name="scoutsgroup", name="group_admin_id"),
    ]
