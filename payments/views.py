import razorpay

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from orders.models import Order
from .models import Payment
from django.shortcuts import redirect
from cart.models import Cart


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


def make_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    amount = int(order.total_amount * 100)

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
    })

    Payment.objects.create(
        order=order,
        razorpay_order_id=razorpay_order["id"],
        amount=order.total_amount,
    )

    context = {
        "order": order,
        "razorpay_order": razorpay_order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(
        request,
        "payment.html",
        context,
    )

def payment_success(request):

    payment = Payment.objects.get(
        razorpay_order_id=request.GET["order_id"]
    )

    payment.razorpay_payment_id = request.GET["payment_id"]

    payment.razorpay_signature = request.GET["signature"]

    payment.status = "Paid"

    payment.save()

    payment.order.status = "Processing"

    payment.order.save()

    return redirect("my_orders")