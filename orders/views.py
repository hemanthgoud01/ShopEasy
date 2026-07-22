from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items.exists():
        return redirect("cart")

    total = sum(item.subtotal() for item in items)

    if request.method == "POST":

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                full_name=request.POST["full_name"],
                phone=request.POST["phone"],
                address=request.POST["address"],
                city=request.POST["city"],
                state=request.POST["state"],
                pincode=request.POST["pincode"],
                total_amount=total,
            )

            for item in items:

                # Check stock availability
                if item.product.stock < item.quantity:
                    return render(
                        request,
                        "checkout.html",
                        {
                            "items": items,
                            "total": total,
                            "error": f"{item.product.name} is out of stock."
                        },
                    )

                # Create Order Item
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

                # Reduce Stock
                

            # Empty Cart

        return redirect("make_payment", order_id=order.id)

    return render(
        request,
        "checkout.html",
        {
            "items": items,
            "total": total,
        },
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders,
        },
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
        },
    )