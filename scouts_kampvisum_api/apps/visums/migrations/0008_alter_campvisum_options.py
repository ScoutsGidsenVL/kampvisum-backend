# Generated by Django 3.2.12 on 2022-04-05 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0007_auto_20220402_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campvisum',
            options={'permissions': [('create_campvisum', 'User can create a camp')]},
        ),
    ]
