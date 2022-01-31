# Generated by Django 3.2.10 on 2022-01-31 10:04

from django.db import migrations, models
import django.db.models.deletion
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('visums', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampLocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
                ('address', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=254)),
                ('is_main_location', models.BooleanField(default=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location_check', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='visums.linkedlocationcheck')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
