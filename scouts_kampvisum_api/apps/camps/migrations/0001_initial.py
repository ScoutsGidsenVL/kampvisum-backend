# Generated by Django 3.2.12 on 2022-03-17 12:12

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
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampYear',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('year', models.IntegerField(verbose_name='year')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_campyear_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_campyear_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
        ),
        migrations.CreateModel(
            name='CampType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('camp_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('is_base', models.BooleanField(default=False)),
                ('is_default', scouts_auth.inuits.models.fields.django_shorthand_model_fields.UniqueBooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_camptype_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_camptype_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['index', 'camp_type'],
            },
        ),
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.TextField()),
                ('start_date', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateField(blank=True, null=True)),
                ('end_date', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_camp_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('sections', models.ManyToManyField(to='groups.ScoutsSection')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_camp_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camps.campyear')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='campyear',
            constraint=models.UniqueConstraint(fields=('year',), name='unique_year'),
        ),
        migrations.AddConstraint(
            model_name='camptype',
            constraint=models.UniqueConstraint(fields=('camp_type',), name='unique_camp_type'),
        ),
    ]
