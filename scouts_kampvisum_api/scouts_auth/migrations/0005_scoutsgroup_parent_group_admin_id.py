# Generated by Django 3.2.12 on 2022-05-06 09:23

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0004_scoutsfunction_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutsgroup',
            name='parent_group_admin_id',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128),
        ),
    ]
