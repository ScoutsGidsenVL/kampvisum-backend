# Generated by Django 3.2.6 on 2021-08-09 11:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.AutoField(db_column='campid', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('uuid', models.UUIDField(default=uuid.UUID('1ba05e12-60bf-45da-843b-80e463445fd9'), editable=False)),
            ],
            options={
                'db_table': 'camps',
                'managed': True,
            },
        ),
    ]