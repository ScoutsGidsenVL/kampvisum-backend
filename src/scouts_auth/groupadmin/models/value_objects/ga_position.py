from django.db import models

from scouts_auth.inuits.models import AbstractNonModel


class GaGeoCoordinate(AbstractNonModel):
    imaginary = models.FloatField()
    real = models.FloatField()

    class Meta:
        abstract = True

    def __init__(self, imaginary: float = 0.0, real: float = 0.0):
        self.imaginary = imaginary
        self.real = real

        # super().__init__([], {})

    def __str__(self):
        return "imaginary({}), real({})".format(self.imaginary, self.real)


class GaPosition(AbstractNonModel):
    latitude: GaGeoCoordinate = models.JSONField()
    longitude: GaGeoCoordinate = models.JSONField()

    class Meta:
        abstract = True

    def __init__(self, latitude: GaGeoCoordinate = None, longitude: GaGeoCoordinate = None):
        self.latitude = latitude
        self.longitude = longitude

        # super().__init__([], {})

    def __str__(self):
        return "latitude({}), longitude({})".format(str(self.latitude), str(self.longitude))
