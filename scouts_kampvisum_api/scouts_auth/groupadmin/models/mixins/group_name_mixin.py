"""app.scouts_auth.groupadmin.models.mixins.group_name_mixin."""

from django.db import models

from scouts_auth.groupadmin.models.fields import GroupAdminIdField
from scouts_auth.inuits.models.fields import RequiredCharField


class GroupNameMixin(models.Model):
    group_name = RequiredCharField()

    class Meta:
        abstract = True
