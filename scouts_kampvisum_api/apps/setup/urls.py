"""apps.setup.urls."""

import rest_framework.routers as drf_routers
import apps.setup.views as setup_views

router = drf_routers.SimpleRouter()
router.register(r"", setup_views.SetupViewSet, "setup")
urlpatterns = router.urls
