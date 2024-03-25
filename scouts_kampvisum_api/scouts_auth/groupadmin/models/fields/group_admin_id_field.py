"""app.scouts_auth.groupadmin.models.fields.group_admin_id_field."""

from scouts_auth.inuits.models.fields import OptionalCharField, RequiredCharField


class GroupAdminIdField(RequiredCharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 48
        super().__init__(*args, **kwargs)


class OptionalGroupAdminIdField(OptionalCharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 48
        super().__init__(*args, **kwargs)
