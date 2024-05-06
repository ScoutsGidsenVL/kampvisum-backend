from apps.locations.views import LocationViewSet
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"locations", LocationViewSet, "locations")

urlpatterns = router.urls
