# Generated by Django 3.2.12 on 2022-04-08 04:53

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('visums', '0011_merge_20220408_0453'),
    ]

    operations = [
        migrations.AddField(
            model_name='campvisum',
            name='approval',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('U', 'UNDECIDED'), ('A', 'APPROVED'), ('N', 'APPROVED_WITH_FEEDBACK'), ('D', 'DISAPPROVED')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='linkedsubcategory',
            name='approval',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('U', 'UNDECIDED'), ('A', 'APPROVED'), ('N', 'APPROVED_WITH_FEEDBACK'), ('D', 'DISAPPROVED')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='linkedsubcategory',
            name='feedback',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, default='', max_length=128),
        ),
    ]
