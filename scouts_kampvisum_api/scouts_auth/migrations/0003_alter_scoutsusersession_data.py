# Generated by Django 4.1.5 on 2023-02-10 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0002_scoutsusersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoutsusersession',
            name='data',
            field=models.JSONField(null=True),
        ),
    ]
