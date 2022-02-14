# Generated by Django 3.2.10 on 2022-02-14 08:16

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
        ('scouts_auth', '0001_initial'),
        ('participants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('camps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampVisum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
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
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
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
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ['camp_year_category_set__camp_year__year'],
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
            name='Check',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('is_multiple', models.BooleanField(default=False)),
                ('is_member', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
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
                'ordering': ['parent__index'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.check')),
            ],
            options={
                'ordering': ['parent__index'],
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
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
                ('contact_name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=128)),
                ('contact_phone', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
                ('contact_email', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=128)),
                ('is_camp_location', models.BooleanField(default=False)),
                ('center_latitude', models.FloatField(blank=True, null=True)),
                ('center_longitude', models.FloatField(blank=True, null=True)),
                ('zoom', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedNumberCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedParticipantCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
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
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('EMPTY', 'Empty'), ('UNCHECKED', 'Unchecked'), ('CHECKED', 'Checked'), ('NOT_APPLICABLE', 'Not applicable')], default='EMPTY', max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('camp_types', models.ManyToManyField(to='camps.CampType')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='visums.category')),
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
                'ordering': ['parent__index'],
            },
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
        migrations.AddField(
            model_name='check',
            name='check_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.checktype'),
        ),
        migrations.AddField(
            model_name='check',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='visums.subcategory'),
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
            name='camp_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_sets', to='camps.camptype'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='camp_year_category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_sets', to='visums.campyearcategoryset'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='categories',
            field=models.ManyToManyField(to='visums.Category'),
        ),
        migrations.AddField(
            model_name='categoryset',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_categoryset_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by'),
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
            name='camp_types',
            field=models.ManyToManyField(to='camps.CampType'),
        ),
        migrations.AddField(
            model_name='category',
            name='camp_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='camps.campyear'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visum', to='visums.linkedcategoryset'),
        ),
        migrations.AlterUniqueTogether(
            name='subcategory',
            unique_together={('name', 'category')},
        ),
        migrations.AddField(
            model_name='linkedparticipantcheck',
            name='value',
            field=models.ManyToManyField(to='participants.InuitsParticipant'),
        ),
        migrations.AddField(
            model_name='linkedfileuploadcheck',
            name='value',
            field=models.ManyToManyField(related_name='checks', to='scouts_auth.PersistedFile'),
        ),
        migrations.AlterUniqueTogether(
            name='check',
            unique_together={('name', 'sub_category')},
        ),
        migrations.AddConstraint(
            model_name='categoryset',
            constraint=models.UniqueConstraint(fields=('camp_year_category_set', 'camp_type'), name='unique_set_for_camp_year_category_set_and_camp_type'),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name', 'camp_year'), name='unique_category_name_and_camp_year'),
        ),
    ]
