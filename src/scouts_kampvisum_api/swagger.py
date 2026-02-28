from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema

from scouts_auth.scouts.permissions import ScoutsFunctionPermissions


class ScoutsFunctionAutoSchema(SwaggerAutoSchema):
    """Adds the 'group' query parameter to endpoints that use ScoutsFunctionPermissions."""

    def get_query_parameters(self):
        params = super().get_query_parameters()

        view = self.view
        permission_classes = getattr(view, "permission_classes", [])
        if any(
            pc is ScoutsFunctionPermissions or (isinstance(pc, type) and issubclass(pc, ScoutsFunctionPermissions))
            for pc in permission_classes
        ):
            params.append(
                openapi.Parameter(
                    "group",
                    openapi.IN_QUERY,
                    description="Group admin ID (e.g. O1306G)",
                    type=openapi.TYPE_STRING,
                )
            )

        return params
