# Generated by Django 3.2.14 on 2022-07-16 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_alter_defaultscoutssectionname_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scoutssection',
            options={'ordering': ['age_group'], 'permissions': [('view_section', 'User can view a group section'), ('edit_section', 'User can create and edit a group section'), ('delete_section', 'User can delete a group section'), ('list_section', 'User can list sections for his/her group')]},
        ),
    ]
