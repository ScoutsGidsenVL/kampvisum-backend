from typing import List

from scouts_auth.groupadmin.models.value_objects import GaFunctionDescription
from scouts_auth.inuits.models import AbstractNonModel


class GaFunctionDescriptionList(AbstractNonModel):
    """
    List of available function types in the GA catalog (GA: lijst van functies).
    Not a paginated response — simply a container returned from the function types endpoint.
    """

    function_descriptions: List[GaFunctionDescription]

    class Meta:
        abstract = True

    def __init__(self, function_descriptions: List[GaFunctionDescription] = None):
        self.function_descriptions = function_descriptions if function_descriptions else []

    def __str__(self):
        return "functions({})".format(
            ", ".join(str(function_description) for function_description in self.function_descriptions),
        )
