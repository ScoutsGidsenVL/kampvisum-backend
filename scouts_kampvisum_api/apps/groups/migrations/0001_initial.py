# Generated by Django 3.2.6 on 2021-08-26 13:28

from django.db import migrations, models
import django.db.models.deletion
import inuits.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('group_admin_id', inuits.models.OptionalCharField(blank=True, max_length=32, unique=True)),
                ('number', inuits.models.OptionalCharField(blank=True, max_length=32)),
                ('name', inuits.models.OptionalCharField(blank=True, max_length=32)),
                ('foundation', inuits.models.OptionalDateTimeField(blank=True, null=True)),
                ('only_leaders', models.BooleanField(default=False)),
                ('show_members_improved', models.BooleanField(default=False)),
                ('email', inuits.models.OptionalCharField(blank=True, max_length=128)),
                ('website', inuits.models.OptionalCharField(blank=True, max_length=128)),
                ('info', inuits.models.OptionalCharField(blank=True, max_length=128)),
                ('public_registration', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['group_admin_id', 'number'],
            },
        ),
        migrations.CreateModel(
            name='SectionName',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('gender', models.CharField(choices=[('X', 'Other'), ('F', 'Female'), ('M', 'Male'), ('H', 'Mixed')], default='H', max_length=1)),
                ('age_group', models.CharField(choices=[('10', 'Leeftijdsgroep 6-9: kapoenen en zeehondjes'), ('15', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 7 jaar'), ('16', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 8 jaar'), ('17', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 9 jaar'), ('20', 'Leeftijdsgroep 8-11: kabouter en (zee)welp'), ('25', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 9 jaar'), ('26', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 10 jaar'), ('27', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 11 jaar'), ('30', 'Leeftijdsgroep 11-14: jonggivers en scheepsmakkers'), ('35', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 12 jaar'), ('36', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 13 jaar'), ('37', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 14 jaar'), ('40', 'Leeftijdsgroep 14-17: gidsen en (zee)verkenners'), ('45', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 15 jaar'), ('46', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 16 jaar'), ('47', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 17 jaar'), ('50', 'Leeftijdsgroep 17-18: jins en loodsen'), ('55', 'Tussentak, leeftijdsgroep 17-18: startleeftijd 18 jaar'), ('60', 'Leeftijdsgroep ouder dan 18, bv. VIPS (akabe)'), ('100', 'Leeftijdsgroep voor leiding, district, gouw, verbond'), ('999', 'Onbekende leeftijdsgroep')], default='10', max_length=3)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['age_group'],
                'unique_together': {('name', 'gender', 'age_group')},
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('hidden', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='groups.group')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='groups.sectionname')),
            ],
            options={
                'ordering': ['name__age_group'],
            },
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(max_length=64)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.grouptype')),
            ],
            options={
                'ordering': ['type'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_type', to='groups.grouptype'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('group_admin_uuid', inuits.models.OptionalCharField(blank=True, max_length=64, unique=True)),
                ('country', inuits.models.OptionalCharField(blank=True, max_length=2)),
                ('postal_code', inuits.models.OptionalCharField(blank=True, max_length=32)),
                ('city', inuits.models.OptionalCharField(blank=True, max_length=64)),
                ('street', inuits.models.OptionalCharField(blank=True, max_length=64)),
                ('number', inuits.models.OptionalCharField(blank=True, max_length=12)),
                ('box', inuits.models.OptionalCharField(blank=True, max_length=12)),
                ('postal_address', models.BooleanField(default=False)),
                ('status', inuits.models.OptionalCharField(blank=True, max_length=12)),
                ('latitude', inuits.models.OptionalCharField(blank=True, max_length=64)),
                ('longitude', inuits.models.OptionalCharField(blank=True, max_length=64)),
                ('description', inuits.models.OptionalCharField(blank=True, max_length=128)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='groups.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultSectionName',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='groups.sectionname')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.grouptype')),
            ],
            options={
                'unique_together': {('type', 'name')},
            },
        ),
    ]
