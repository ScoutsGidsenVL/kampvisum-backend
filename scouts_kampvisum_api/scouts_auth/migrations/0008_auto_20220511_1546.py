# Generated by Django 3.2.12 on 2022-05-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0007_auto_20220511_1529'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='scoutsfunction',
            name='unique_group_admin_id',
        ),
        migrations.AddConstraint(
            model_name='scoutsfunction',
            constraint=models.UniqueConstraint(fields=('user', 'group_admin_id'), name='unique_user_for_function'),
        ),
    ]