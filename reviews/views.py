from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Review
from products.models import Product


@login_required
def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":

        rating = request.POST["rating"]
        comment = request.POST["comment"]

        Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                "rating": rating,
                "comment": comment,
            }
        )

        return redirect("product_detail", product_id=product.id)

    return redirect("product_detail", product_id=product.id)