"""apps.camps.urls"""

from rest_framework import routers

from apps.camps.views import CampTypeViewSet, CampViewSet, CampYearViewSet

router = routers.SimpleRouter()

router.register(r"camps", CampViewSet, "camp")
router.register(r"camp_years", CampYearViewSet, "camp")
router.register(r"camp_types", CampTypeViewSet, "camp_types")

urlpatterns = router.urls
