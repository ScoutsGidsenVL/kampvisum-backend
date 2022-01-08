# Generated by Django 3.2.10 on 2022-01-08 10:17

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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scouts_auth', '0001_initial'),
        ('groups', '0001_initial'),
        ('camps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampVisum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['camp__sections__name__age_group'],
            },
        ),
        migrations.CreateModel(
            name='CampYearCategorySet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredIntegerField(default=0)),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='CategorySet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['category_set__camp_year__year'],
            },
        ),
        migrations.CreateModel(
            name='CategorySetPriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.CharField(default='Verbond', max_length=32, unique=True)),
                ('priority', models.IntegerField(default=100)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='CheckType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('check_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=32)),
            ],
            options={
                'ordering': ['check_type'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinkedCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='visums.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCommentCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedDateCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedDurationCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('start_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
                ('end_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedFileUploadCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedLocationCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedLocationContactCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedMemberCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedSimpleCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('UNCHECKED', 'Unchecked'), ('CHECKED', 'Checked'), ('NOT_APPLICABLE', 'Not applicable')], default='UNCHECKED', max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='VisumCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('check_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.checktype')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='visums.subcategory')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LinkedSubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='visums.linkedcategory')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.subcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linkedcheck',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.visumcheck'),
        ),
        migrations.AddField(
            model_name='linkedcheck',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='visums.linkedsubcategory'),
        ),
        migrations.CreateModel(
            name='LinkedCategorySet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.categoryset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='visums.linkedcategoryset'),
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.category'),
        ),
        migrations.AddConstraint(
            model_name='checktype',
            constraint=models.UniqueConstraint(fields=('check_type',), name='unique_check_type'),
        ),
        migrations.AddConstraint(
            model_name='categorysetpriority',
            constraint=models.UniqueConstraint(fields=('owner',), name='unique_owner'),
        ),
        migrations.AddConstraint(
            model_name='categorysetpriority',
            constraint=models.UniqueConstraint(fields=('priority',), name='unique_priority'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_sets', to='visums.campyearcategoryset'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_categoryset_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='group_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='priority',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='visums.categorysetpriority'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_categoryset_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by'),
        ),
        migrations.AddField(
            model_name='category',
            name='category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='visums.categoryset'),
        ),
        migrations.AddField(
            model_name='campyearcategoryset',
            name='camp_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='camp_year_category_set', to='camps.campyear'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='camp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camps.camp'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.linkedcategoryset'),
        ),
        migrations.AlterUniqueTogether(
            name='visumcheck',
            unique_together={('name', 'sub_category')},
        ),
        migrations.AlterUniqueTogether(
            name='subcategory',
            unique_together={('name', 'category')},
        ),
        migrations.AddField(
            model_name='linkedfileuploadcheck',
            name='value',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scouts_auth.persistedfile'),
        ),
        migrations.AddConstraint(
            model_name='categoryset',
            constraint=models.UniqueConstraint(fields=('category_set', 'group_type'), name='unique_set_for_category_set_and_group_type'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'category_set')},
        ),
    ]