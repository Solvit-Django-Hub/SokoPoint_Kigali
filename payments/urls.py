from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('process/', PaymentView.as_view(), name='process-payment'),
]
