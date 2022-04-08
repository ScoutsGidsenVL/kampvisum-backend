# Generated by Django 3.2.12 on 2022-04-02 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visums', '0006_alter_campvisum_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampVisumEngagement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
                ('district_commissioner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumengagement_district_commissioner', to=settings.AUTH_USER_MODEL)),
                ('group_leaders', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumengagement_group_leaders', to=settings.AUTH_USER_MODEL)),
                ('leaders', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='campvisumengagement_leaders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='campvisum',
            name='approval',
        ),
        migrations.DeleteModel(
            name='CampVisumApproval',
        ),
        migrations.AddField(
            model_name='campvisum',
            name='engagement',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visum', to='visums.campvisumengagement'),
        ),
    ]