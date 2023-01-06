# Generated by Django 3.2.16 on 2023-01-05 10:22

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camplocation',
            name='country',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='camplocation',
            name='house_number',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='camplocation',
            name='postalcode',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='camplocation',
            name='street',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='camplocation',
            name='township',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254),
        ),
    ]
