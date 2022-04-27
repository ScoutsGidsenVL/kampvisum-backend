# Generated by Django 3.2.12 on 2022-04-19 08:49

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0016_alter_campvisum_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campvisum',
            options={'permissions': [('view_visum', 'User can view a camp visum'), ('edit_visum', 'User can create and edit a camp visum'), ('list_visum', 'User can list visums for his/her group'), ('view_visum_notes', 'User is a DC and can view approval notes'), ('edit_visum_notes', 'User is a DC and can edit approval notes')]},
        ),
        migrations.AlterModelOptions(
            name='linkedcategory',
            options={'ordering': ['parent__index']},
        ),
        migrations.RemoveField(
            model_name='linkedcategory',
            name='notes',
        ),
        migrations.AddField(
            model_name='campvisum',
            name='notes',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128),
        ),
    ]