# Generated by Django 3.2.12 on 2022-03-23 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampVisumApproval',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
                ('district_commissioner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumapproval_district_commissioner', to=settings.AUTH_USER_MODEL)),
                ('group_leaders', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumapproval_group_leaders', to=settings.AUTH_USER_MODEL)),
                ('leaders', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumapproval_leaders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='campvisum',
            name='approval',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visum', to='visums.campvisumapproval'),
        ),
    ]
