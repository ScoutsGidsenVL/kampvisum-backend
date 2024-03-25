"""apps.scouts_auth.permissions.extended_django_model_permission."""

from rest_framework import permissions


class ExtendedDjangoModelPermission(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.read_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.read_%(model_name)s"],
        "HEAD": ["%(app_label)s.read_%(model_name)s"],
        "POST": ["%(app_label)s.create_%(model_name)s"],
        "PUT": ["%(app_label)s.update_%(model_name)s"],
        "PATCH": ["%(app_label)s.update_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
