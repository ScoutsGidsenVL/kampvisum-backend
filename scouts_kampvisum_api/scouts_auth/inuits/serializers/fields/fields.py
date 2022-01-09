from rest_framework import serializers

from scouts_auth.inuits.serializers.fields import DatetypeAwareDateSerializerField


class OptionalCharSerializerField(serializers.CharField):
    """
    Initializes a serializers.CharField that is optional.

    This is equivalent to setting a serializer.CharField as such:
    some_optional_char_field = serializers.CharField(
        default=empty, required=False, allow_blank=True, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = serializers.empty
        kwargs["required"] = False
        kwargs["allow_blank"] = True
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)


class DefaultCharSerializerField(serializers.CharField):
    """
    Initializes a serializers.CharField as optional with a default.

    This is equivalent to setting a serializers.CharField as such:
    some_optional_char_field = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, default=<some_default_value>
    )
    If max_length is not specified, it is set to 128.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        kwargs["required"] = False
        kwargs["allow_blank"] = True
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)


class OptionalIntegerSerializerField(serializers.IntegerField):
    """
    Initializes a serializers.IntegerField that is optional.

    This is equivalent to setting a serializer.IntegerField as such:
    some_optional_integer_field = serializers.IntegerField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = serializers.empty
        kwargs["required"] = False
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)


class RequiredIntegerSerializerField(serializers.IntegerField):
    """
    Initializes a serializers.IntegerField that is required.

    This is equivalent to setting a serializer.IntegerField as such:
    some_optional_integer_field = serializers.IntegerField(
        required=True, allow_null=False
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["required"] = True
        kwargs["allow_null"] = False
        super().__init__(*args, **kwargs)


class OptionalChoiceSerializerField(serializers.ChoiceField):
    """
    Initializes a serializers.ChoiceField that is optional.

    This is equivalent to setting a serializer.ChoiceField as such:
    some_optional_choice_field = serializers.ChoiceField(
        default=empty, required=False, allow_blank=True, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = serializers.empty
        kwargs["required"] = True
        kwargs["allow_blank"] = True
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)


class RequiredYearSerializerField(serializers.IntegerField):
    """
    Initializes a serializers.IntegerField that represents a required year.

    This is equivalent to setting a serializer.IntegerField as such:
    some_required_year_field = serializers.IntegerField(
        min_value=2021, max_value=2121, required=True,allow_null=False
    )
    Note the assumption that the Scouts will be using a different app by 2121.
    """

    def __init__(self, *args, **kwargs):
        kwargs["min_value"] = 2021
        kwargs["max_value"] = 2121
        kwargs["required"] = True
        kwargs["allow_null"] = False
        super().__init__(*args, **kwargs)


class OptionalDateSerializerField(DatetypeAwareDateSerializerField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = serializers.empty
        kwargs["required"] = False
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)


class OptionalDateTimeSerializerField(serializers.DateTimeField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = serializers.empty
        kwargs["required"] = False
        kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)
