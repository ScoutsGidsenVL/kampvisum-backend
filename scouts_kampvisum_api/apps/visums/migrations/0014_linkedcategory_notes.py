# Generated by Django 3.2.12 on 2022-04-08 05:23

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0013_alter_linkedsubcategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedcategory',
            name='notes',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128),
        ),
    ]
