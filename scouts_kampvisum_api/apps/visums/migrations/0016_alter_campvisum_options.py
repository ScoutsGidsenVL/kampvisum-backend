# Generated by Django 3.2.12 on 2022-04-08 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0015_auto_20220408_0531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campvisum',
            options={'permissions': [('view_visum', 'User can view a camp visum'), ('edit_visum', 'User can create and edit a camp visum'), ('list_visum', 'User can list visums for his/her group')]},
        ),
    ]
