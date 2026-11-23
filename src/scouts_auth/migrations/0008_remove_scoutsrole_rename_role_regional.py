from django.db import migrations


OLD_ROLE = "role_shire_president"
NEW_ROLE = "role_regional"


def _rename_role(apps, old_name: str, new_name: str):
    """
    Renames the auth group of a role, keeping its members.

    PermissionService only does get_or_create on the names in roles.yaml, so without this
    the old group would linger and its members would lose the role until their next login.
    """
    Group = apps.get_model("auth", "Group")

    old_group = Group.objects.filter(name=old_name).first()
    if not old_group:
        return

    new_group = Group.objects.filter(name=new_name).first()
    if not new_group:
        old_group.name = new_name
        old_group.save()
        return

    # Both exist (e.g. roles.yaml was loaded before this migration ran): move the members
    for user in old_group.user_set.all():
        user.groups.add(new_group)
    old_group.delete()


def forwards(apps, schema_editor):
    _rename_role(apps, OLD_ROLE, NEW_ROLE)


def backwards(apps, schema_editor):
    _rename_role(apps, NEW_ROLE, OLD_ROLE)


class Migration(migrations.Migration):
    """
    Roles are derived from the responsibilities in groepsadmin (GA: verantwoordelijkheden) instead of
    the functions of the user.

    - ScoutsRole is no longer used. It is an unmanaged model, so deleting it only updates the
      migration state.
    - role_shire_president becomes role_regional: it now covers everyone with the responsibility
      "regionaal" (gouwbureau and its adjuncts, DC's).
    """

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("scouts_auth", "0007_remove_scoutsgroup_group_admin_id"),
    ]

    operations = [
        migrations.DeleteModel(name="ScoutsRole"),
        migrations.RunPython(forwards, backwards),
    ]
