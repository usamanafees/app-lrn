from rest_framework.routers import DefaultRouter
from .views import LineItemCalculateView, LineItemViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'line-items', LineItemViewSet)


urlpatterns = [
    path('line-items/calculate/', LineItemCalculateView.as_view(), name='line-item-calculate'),
] + router.urls