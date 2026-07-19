from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from products.models import Product
from orders.models import Order
from django.contrib.auth.models import User
from django.db.models import Sum


@staff_member_required
def dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_customers = User.objects.count()

 

    revenue = (
        Order.objects
        .exclude(status="Cancelled")
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    low_stock = Product.objects.filter(stock__lt=5)

    recent_orders = (
        Order.objects
        .order_by("-created_at")[:5]
    )

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "revenue": revenue,
        "low_stock": low_stock,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )