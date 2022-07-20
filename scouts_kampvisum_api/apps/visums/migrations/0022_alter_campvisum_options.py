# Generated by Django 3.2.12 on 2022-07-04 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0021_auto_20220506_0923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campvisum',
            options={'permissions': [('view_camp_locations', 'User can view all camp locations'), ('view_visum', 'User can view a camp visum'), ('edit_visum', 'User can create and edit a camp visum'), ('list_visum', 'User can list visums for his/her group'), ('view_visum_notes', 'User is a DC and can view approval notes'), ('edit_visum_notes', 'User is a DC and can edit approval notes')]},
        ),
    ]