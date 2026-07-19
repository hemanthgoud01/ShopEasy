from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.all()

    total = sum(item.subtotal() for item in items)

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
        },
    )


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    item.delete()

    return redirect("cart")


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    item.quantity += 1
    item.save()

    return redirect("cart")


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")