import json

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsUserSession, ScoutsGroup

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSessionSerializer:
    """Serializes a session stored user instance to a string."""

    @staticmethod
    def to_user_session(scouts_user: ScoutsUser) -> str:
        if ScoutsUser is None:
            return ""

        scouts_user.full_clean()
        scouts_user.save()

        data = {}

        data["scouts_groups"] = []
        for scouts_group in scouts_user._scouts_groups:
            data["scouts_groups"].append({
                "number": scouts_group.number,
                "name": scouts_group.name,
                "type": scouts_group.type,
                "responsibilities": scouts_group.responsibilities or [],
            })

        return json.dumps(data, default=str)

    @staticmethod
    def to_scouts_user(session: ScoutsUserSession) -> dict:
        """
        Returns the session data, or an empty dict if the session can't be used.

        Sessions written before roles were derived from the responsibilities (GA: verantwoordelijkheden)
        hold no responsibilities. Using them would leave the user without roles, so they are discarded
        and the user is rebuilt from groepsadmin.
        """
        if not session:
            return {}

        data: dict = json.loads(json.loads(session.data))

        groups = data.get("scouts_groups", [])
        if any("responsibilities" not in group for group in groups):
            logger.debug("USER SESSION - Discarding session without responsibilities")
            return {}

        deserialized = {}

        deserialized["scouts_groups"] = []
        for group in groups:
            scouts_group = ScoutsGroup()

            scouts_group.number = group.get("number")
            scouts_group.name = group["name"]
            scouts_group.type = group["type"]
            scouts_group.responsibilities = group["responsibilities"] or []

            deserialized["scouts_groups"].append(scouts_group)

        return deserialized
