from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth

from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order, OrderItem


@staff_member_required
def dashboard(request):

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_revenue = Order.objects.aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    recent_orders = Order.objects.order_by("-created_at")[:10]

    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    monthly_sales = (
        Order.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    status_counts = (
        Order.objects
        .values("status")
        .annotate(count=Count("id"))
    )

    context = {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "top_products": top_products,

        "monthly_sales": monthly_sales,
        "status_counts": status_counts,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )