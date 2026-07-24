from rest_framework.routers import DefaultRouter
from .views import LineItemViewSet

router = DefaultRouter()
router.register(r'line-items', LineItemViewSet)


urlpatterns = router.urls