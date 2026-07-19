from django.db import models
from orders.models import Order


class Payment(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    razorpay_order_id = models.CharField(max_length=200)

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    razorpay_signature = models.CharField(
        max_length=500,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.razorpay_order_id