# Generated by Django 4.1.5 on 2023-02-10 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.groupadmin.models.fields.group_admin_id_field
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InuitsParticipant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('first_name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=32)),
                ('last_name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('phone_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=24)),
                ('cell_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=24)),
                ('email', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalEmailField(blank=True, default='', max_length=254, null=True)),
                ('birth_date', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateField(blank=True, null=True)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('X', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('street', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=100)),
                ('number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=5)),
                ('letter_box', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=5)),
                ('postal_code', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128)),
                ('city', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=40)),
                ('group_group_admin_id', scouts_auth.groupadmin.models.fields.group_admin_id_field.OptionalGroupAdminIdField(blank=True, default='', max_length=48, null=True)),
                ('group_admin_id', scouts_auth.groupadmin.models.fields.group_admin_id_field.OptionalGroupAdminIdField(blank=True, default='', max_length=48, null=True)),
                ('is_member', models.BooleanField(default=False)),
                ('comment', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=300)),
                ('inactive_member', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['first_name', 'last_name', 'birth_date', 'group_group_admin_id'],
            },
        ),
        migrations.CreateModel(
            name='VisumParticipant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('participant_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('P', 'participant'), ('M', 'member'), ('C', 'cook'), ('L', 'leader'), ('R', 'responsible'), ('A', 'adult')], default='P', max_length=1)),
                ('payment_status', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('Y', 'YES'), ('N', 'NO'), ('X', 'NOT_APPLICABLE')], default='N', max_length=1)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visum_participant', to='participants.inuitsparticipant')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['participant__first_name', 'participant__last_name', 'participant__birth_date', 'participant__group_group_admin_id'],
            },
        ),
        migrations.AddConstraint(
            model_name='inuitsparticipant',
            constraint=models.UniqueConstraint(condition=models.Q(('email__isnull', False), models.Q(('email__exact', ''), _negated=True)), fields=('group_group_admin_id', 'email'), name='unique_group_and_email_if_email_present'),
        ),
    ]
