from django.shortcuts import render, get_object_or_404
from .models import Product


from django.http import HttpResponse


from django.shortcuts import render

def home(request):
    try:
        products = Product.objects.all()
        return render(request, "home.html", {"products": products})
    except Exception as e:
        from django.http import HttpResponse
        import traceback
        return HttpResponse(f"<pre>{traceback.format_exc()}</pre>")

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(request, "product_detail.html", {
        "product": product
    })