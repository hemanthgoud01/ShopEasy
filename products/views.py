from django.shortcuts import render, get_object_or_404
from .models import Product


from django.http import HttpResponse

def home(request):
    return HttpResponse("ShopEasy is working!")

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(request, "product_detail.html", {
        "product": product
    })