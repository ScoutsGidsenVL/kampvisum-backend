# Generated by Django 4.1.5 on 2023-02-28 12:53

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoutsusersession',
            name='username',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128, unique=True),
        ),
    ]