"""apps.setup.urls."""

import apps.setup.views as setup_views
import rest_framework.routers as drf_routers

router = drf_routers.SimpleRouter()
router.register(r"", setup_views.SetupViewSet, "setup")
urlpatterns = router.urls
