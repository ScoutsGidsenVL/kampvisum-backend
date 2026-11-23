from django.db import migrations, models


class Migration(migrations.Migration):
    """The column holds the groepsnummer of the participant's group (e.g. X9010G), the new name says so."""

    dependencies = [
        ("participants", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inuitsparticipant",
            old_name="group_group_admin_id",
            new_name="group_number",
        ),
        migrations.AlterModelOptions(
            name="inuitsparticipant",
            options={"ordering": ["first_name", "last_name", "birth_date", "group_number"]},
        ),
        migrations.AlterModelOptions(
            name="visumparticipant",
            options={
                "ordering": [
                    "participant__first_name",
                    "participant__last_name",
                    "participant__birth_date",
                    "participant__group_number",
                ]
            },
        ),
        # PostgreSQL updates the unique index itself when the column is renamed,
        # so only the migration state needs the new field name.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveConstraint(
                    model_name="inuitsparticipant",
                    name="unique_group_and_email_if_email_present",
                ),
                migrations.AddConstraint(
                    model_name="inuitsparticipant",
                    constraint=models.UniqueConstraint(
                        condition=models.Q(("email__isnull", False), models.Q(("email__exact", ""), _negated=True)),
                        fields=("group_number", "email"),
                        name="unique_group_and_email_if_email_present",
                    ),
                ),
            ],
        ),
    ]
