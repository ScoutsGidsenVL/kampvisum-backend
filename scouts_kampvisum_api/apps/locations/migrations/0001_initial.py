<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 4.1.5 on 2023-02-06 16:38
=======
# Generated by Django 4.1.5 on 2023-02-06 09:22
>>>>>>> 6ecc7d7 (fix: clean migrations)
=======
# Generated by Django 4.1.5 on 2023-02-06 16:38
>>>>>>> 73bbf1e (fix: clean migrations)

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedLocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=64)),
                ('contact_name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128)),
                ('contact_phone', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=64)),
                ('contact_email', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalEmailField(blank=True, default='', max_length=128, null=True)),
                ('is_camp_location', models.BooleanField(default=False)),
                ('center_latitude', models.FloatField(blank=True, default=50.4956754, null=True)),
                ('center_longitude', models.FloatField(blank=True, default=3.3452037, null=True)),
                ('zoom', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=7, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CampLocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=64)),
                ('address', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('is_main_location', models.BooleanField(default=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('country', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('postalcode', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('township', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('street', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('house_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=254)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='locations.linkedlocation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
