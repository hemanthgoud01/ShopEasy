from django.urls import path
from . import views

urlpatterns = [
    path(
        "pay/<int:order_id>/",
        views.make_payment,
        name="make_payment",
    ),

    path(
        "success/",
        views.payment_success,
        name="payment_success",
    ),
]