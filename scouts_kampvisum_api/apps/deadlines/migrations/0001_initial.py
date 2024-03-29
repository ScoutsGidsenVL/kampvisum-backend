# Generated by Django 4.1.5 on 2023-02-17 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.inuits.models.fields.datetype_aware_date_field
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('visums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('camps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('is_important', models.BooleanField(default=False)),
                ('is_camp_registration', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['index', 'due_date__date_year', 'due_date__date_month', 'due_date__date_day', 'is_important', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DeadlineDate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_day', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_month', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_year', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('calculated_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField()),
            ],
            options={
                'ordering': ['date_year', 'date_month', 'date_day'],
            },
        ),
        migrations.CreateModel(
            name='DeadlineFlag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('change_handlers', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True, default='')),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('flag', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['index', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DeadlineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('deadline_item_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('D', 'Deadline'), ('C', 'LinkedCheck deadline'), ('S', 'LinkedSubCategory deadline')], default='D', max_length=1)),
                ('deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='deadlines.deadline')),
                ('item_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visums.check')),
                ('item_flag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_item', to='deadlines.deadlineflag')),
                ('item_sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visums.subcategory')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='LinkedDeadline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline', to='deadlines.deadline')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
                ('visum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='visums.campvisum')),
            ],
            options={
                'ordering': ['parent'],
            },
        ),
        migrations.CreateModel(
            name='LinkedDeadlineFlag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('flag', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deadlines.deadlineflag')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinkedDeadlineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('flag', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_item', to='deadlines.linkeddeadlineflag')),
                ('linked_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_items', to='visums.linkedcheck')),
                ('linked_deadline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='deadlines.linkeddeadline')),
                ('linked_sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_items', to='visums.linkedsubcategory')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline_item', to='deadlines.deadlineitem')),
            ],
            options={
                'ordering': ['parent__index'],
            },
        ),
        migrations.AddConstraint(
            model_name='deadlineflag',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_deadline_flag_name'),
        ),
        migrations.AddField(
            model_name='deadlinedate',
            name='deadline',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='due_date', to='deadlines.deadline'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='camp_types',
            field=models.ManyToManyField(related_name='deadlines', to='camps.camptype'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='camp_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline_set', to='camps.campyear'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterUniqueTogether(
            name='linkeddeadline',
            unique_together={('parent', 'visum')},
        ),
        migrations.AddConstraint(
            model_name='deadlineitem',
            constraint=models.UniqueConstraint(condition=models.Q(('item_sub_category', None), ('item_check', None)), fields=('deadline', 'deadline_item_type', 'item_flag'), name='unique_deadline_type_and_flag_if_null_sub_category_and_null_check'),
        ),
        migrations.AddConstraint(
            model_name='deadlineitem',
            constraint=models.UniqueConstraint(condition=models.Q(('item_flag', None), ('item_check', None)), fields=('deadline', 'deadline_item_type', 'item_sub_category'), name='unique_deadline_type_and_sub_category_if_null_flag_and_null_check'),
        ),
        migrations.AddConstraint(
            model_name='deadlineitem',
            constraint=models.UniqueConstraint(condition=models.Q(('item_flag', None), ('item_sub_category', None)), fields=('deadline', 'deadline_item_type', 'item_check'), name='unique_deadline_type_and_check_if_null_flag_and_null_sub_category'),
        ),
        migrations.AddConstraint(
            model_name='deadlinedate',
            constraint=models.UniqueConstraint(fields=('deadline',), name='unique_deadline'),
        ),
        migrations.AddConstraint(
            model_name='deadline',
            constraint=models.UniqueConstraint(fields=('name', 'camp_year'), name='unique_name__camp_year'),
        ),
    ]
