import json

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsUserSession, ScoutsGroup, ScoutsRole

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
                "_child_group_names": ",".join(
                    [name for name in scouts_group._child_group_names] if scouts_group._child_group_names else ""
                ),
                "type": scouts_group.type,
            })

        data["scouts_functions"] = []
        for scouts_function in scouts_user._scouts_functions:
            data["scouts_functions"].append({
                "group_admin_id": scouts_function.group_admin_id,
                "end": scouts_function.end,
                "scouts_group": scouts_function.scouts_group,
                "code": scouts_function.code,
                "description": scouts_function.description,
                "is_leader": scouts_function.is_leader,
            })

        return json.dumps(data, default=str)

    @staticmethod
    def to_scouts_user(session: ScoutsUserSession) -> dict:
        if not session:
            return {}

        data: dict = json.loads(json.loads(session.data))
        deserialized = {}

        deserialized["scouts_groups"] = []
        for group in data["scouts_groups"]:
            scouts_group = ScoutsGroup()

            # Sessions written before the switch to the groepsnummer may only hold "group_admin_id"
            scouts_group.number = group.get("number") or group.get("group_admin_id")
            scouts_group.name = group["name"]
            scouts_group._child_group_names = (
                group["_child_group_names"].split(",") if group["_child_group_names"] else []
            )
            scouts_group.type = group["type"]

            deserialized["scouts_groups"].append(scouts_group)

        deserialized["scouts_functions"] = []
        for function in data["scouts_functions"]:
            scouts_function = ScoutsRole()

            scouts_function.group_admin_id = function["group_admin_id"]
            scouts_function.end = function["end"]
            scouts_function.scouts_group = function["scouts_group"]
            scouts_function.code = function["code"]
            scouts_function.description = function["description"]
            scouts_function.is_leader = function["is_leader"]

            deserialized["scouts_functions"].append(scouts_function)

        return deserialized
