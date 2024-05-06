from apps.groups.views import ScoutsSectionViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"sections", ScoutsSectionViewSet, "sections")

urlpatterns = router.urls
