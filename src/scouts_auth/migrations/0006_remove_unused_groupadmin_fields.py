from django.db import migrations


class Migration(migrations.Migration):
    """
    Removes fields copied from Groepsadmin that the app never reads.

    Only the ScoutsUser fields are real database columns. ScoutsGroup and ScoutsRole are
    unmanaged models (managed = False), so their RemoveField operations only update the
    migration state.
    """

    dependencies = [
        ("scouts_auth", "0005_scoutsrole_delete_scoutsfunction"),
    ]

    operations = [
        migrations.RemoveField(model_name="scoutsuser", name="gender"),
        migrations.RemoveField(model_name="scoutsuser", name="phone_number"),
        migrations.RemoveField(model_name="scoutsuser", name="membership_number"),
        migrations.RemoveField(model_name="scoutsuser", name="customer_number"),
        migrations.RemoveField(model_name="scoutsuser", name="birth_date"),
        migrations.RemoveField(model_name="scoutsgroup", name="email"),
        migrations.RemoveField(model_name="scoutsgroup", name="website"),
        migrations.RemoveField(model_name="scoutsgroup", name="parent_group"),
        migrations.RemoveField(model_name="scoutsrole", name="begin"),
        migrations.RemoveField(model_name="scoutsrole", name="type"),
        migrations.RemoveField(model_name="scoutsrole", name="max_birth_date"),
        migrations.RemoveField(model_name="scoutsrole", name="adjunct"),
    ]
