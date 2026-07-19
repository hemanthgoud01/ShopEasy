from django.shortcuts import render, get_object_or_404
from .models import Product


from django.http import HttpResponse
from .models import Product

def home(request):
    try:
        products = Product.objects.all()
        return HttpResponse(f"Products count: {products.count()}")
    except Exception as e:
        return HttpResponse(str(e))

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(request, "product_detail.html", {
        "product": product
    })