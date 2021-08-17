# Generated by Django 3.2.6 on 2021-08-17 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_groups', '0003_alter_scoutsdefaultsectionname_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutssection',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scoutssection',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='scouts_groups.scoutsgroup'),
        ),
    ]
