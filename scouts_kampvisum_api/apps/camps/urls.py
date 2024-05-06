from apps.camps.views import CampTypeViewSet
from apps.camps.views import CampViewSet
from apps.camps.views import CampYearViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"camps", CampViewSet, "camp")
router.register(r"camp_years", CampYearViewSet, "camp")
router.register(r"camp_types", CampTypeViewSet, "camp_types")

urlpatterns = router.urls
