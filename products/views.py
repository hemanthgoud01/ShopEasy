from django.shortcuts import render, get_object_or_404
from .models import Product,Category
from reviews.models import Review
from django.db.models import Avg


from django.http import HttpResponse


from django.shortcuts import render

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = request.GET.get("category")

    if selected_category:
        products = products.filter(category_id=selected_category)
        selected_category = int(selected_category)
    else:
        selected_category = None

    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
    }

    return render(request, "home.html", context)

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = product.reviews.all().order_by("-created_at")

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "average_rating": average_rating,
        },
    )