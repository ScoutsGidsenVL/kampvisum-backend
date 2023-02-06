<<<<<<< HEAD
# Generated by Django 4.1.5 on 2023-02-06 16:38
=======
# Generated by Django 4.1.5 on 2023-02-06 09:22
>>>>>>> 6ecc7d7 (fix: clean migrations)

from django.db import migrations, models
import django.db.models.deletion
import scouts_auth.groupadmin.models.fields.group_admin_id_field
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(default='', max_length=128)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('X', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age_group', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ScoutsGroupType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('is_default', scouts_auth.inuits.models.fields.django_shorthand_model_fields.UniqueBooleanField(default=False)),
            ],
            options={
                'ordering': ['group_type'],
            },
        ),
        migrations.CreateModel(
            name='ScoutsSection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group', scouts_auth.groupadmin.models.fields.group_admin_id_field.GroupAdminIdField(max_length=48)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('X', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age_group', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['age_group'],
                'permissions': [('create_section', 'User can create a group section'), ('read_section', 'User can view a group section'), ('update_section', 'User can edit a group section'), ('delete_section', 'User can delete a group section'), ('list_section', 'User can list sections for his/her group')],
            },
        ),
        migrations.CreateModel(
            name='ScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('X', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age_group', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['age_group'],
            },
        ),
        migrations.AddConstraint(
            model_name='scoutssectionname',
            constraint=models.UniqueConstraint(fields=('name', 'gender', 'age_group'), name='unique_name_gender_and_age_group'),
        ),
        migrations.AddField(
            model_name='scoutssection',
            name='section_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='groups.scoutssectionname'),
        ),
        migrations.AddField(
            model_name='scoutsgrouptype',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype'),
        ),
        migrations.AddField(
            model_name='defaultscoutssectionname',
            name='group_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype'),
        ),
        migrations.AddConstraint(
            model_name='scoutssection',
            constraint=models.UniqueConstraint(fields=('group', 'name', 'gender', 'age_group'), name='unique_group_name_gender_age_group_for_section'),
        ),
        migrations.AddConstraint(
            model_name='scoutsgrouptype',
            constraint=models.UniqueConstraint(fields=('group_type',), name='unique_group_type'),
        ),
        migrations.AddConstraint(
            model_name='defaultscoutssectionname',
            constraint=models.UniqueConstraint(fields=('group_type', 'name', 'gender', 'age_group'), name='unique_group_type_and_name_gender_age_group_for_default_scouts_section_name'),
        ),
    ]
