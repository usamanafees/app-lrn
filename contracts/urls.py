from django.urls import path
from .views import ContractsWithMetersSlowView, ContractsWithMetersFastView

urlpatterns = [
    path('contracts/with-meters-slow/', ContractsWithMetersSlowView.as_view()),
    path('contracts/with-meters-fast/', ContractsWithMetersFastView.as_view()),
]