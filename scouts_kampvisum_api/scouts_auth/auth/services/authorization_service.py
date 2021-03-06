from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AuthorizationService:

    SUPER_ADMIN = "role_super_admin"

    def add_user_to_group(
        self,
        user: settings.AUTH_USER_MODEL,
        group: Group = None,
        group_name: str = None,
    ) -> settings.AUTH_USER_MODEL:
        if not group and not group_name:
            raise ValueError("Group or group name must be supplied")

        if not group:
            try:
                group: Group = Group.objects.get(name=group_name)
            except ObjectDoesNotExist:
                logger.error("Auth group with name %s does not exist", group_name)
                raise Exception

        logger.debug("Adding user %s to auth group %s", user.username, group.name)
        group.user_set.add(user)

        if group.name == self.SUPER_ADMIN:
            user.is_superuser = True

        user.full_clean()
        user.save()

        return user

    def remove_user_from_group(
        self,
        user: settings.AUTH_USER_MODEL,
        group: Group = None,
        group_name: str = None,
    ) -> settings.AUTH_USER_MODEL:
        if not group and not group_name:
            raise ValueError("Group or group name must be supplied")

        if not group:
            try:
                group: Group = Group.objects.get(name=group_name)
            except ObjectDoesNotExist:
                logger.error("Auth group with name %s does not exist", group_name)
                raise Exception

        logger.debug("Removing user %s from auth group %s", user.username, group.name)
        group.user_set.remove(user)

        user.full_clean()
        user.save()

        return user
