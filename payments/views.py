import razorpay

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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

@login_required
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


@login_required
def payment_success(request):

    payment = Payment.objects.get(
        razorpay_order_id=request.GET["order_id"]
    )

    params = {
        "razorpay_order_id": request.GET["order_id"],
        "razorpay_payment_id": request.GET["payment_id"],
        "razorpay_signature": request.GET["signature"],
    }

    try:
        # Verify payment signature
        client.utility.verify_payment_signature(params)

        payment.razorpay_payment_id = params["razorpay_payment_id"]
        payment.razorpay_signature = params["razorpay_signature"]
        payment.status = "Paid"
        payment.save()

        payment.order.status = "Processing"
        payment.order.save()

        # Reduce stock after successful payment
        for item in payment.order.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        # Clear user's cart
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            cart.items.all().delete()

        return render(
            request,
            "payment_success.html",
            {
                 "order": payment.order,
                "payment": payment,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        payment.status = "Failed"
        payment.save()

        return render(
            request,
            "payment_failed.html",
            {
                "message": "Payment verification failed."
            }
        )
    

@login_required
def payment_failed(request):
    return render(request, "payment_failed.html")