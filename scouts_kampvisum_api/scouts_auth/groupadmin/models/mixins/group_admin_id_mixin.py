"""app.scouts_auth.groupadmin.models.mixins.group_admin_id_mixin."""

from django.db import models

from scouts_auth.groupadmin.models.fields import GroupAdminIdField


class GroupAdminIdMixin(models.Model):
    group = GroupAdminIdField()

    class Meta:
        abstract = True
