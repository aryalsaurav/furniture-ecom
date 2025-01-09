# shop/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Furniture, Order, Category


def home_view(request):
    """Home page showing a few recent or featured items."""
    recent_furniture = Furniture.objects.filter(is_sold=False).order_by("-created_at")[
        :6
    ]
    categories = Category.objects.all()[:3]
    return render(
        request,
        "shop/home.html",
        {"recent_furniture": recent_furniture, "categories": categories},
    )


def product_list_view(request):
    """List all furniture that is not sold."""
    category = request.GET.get("category")
    furniture_list = Furniture.objects.filter(is_sold=False)
    categories = Category.objects.all()
    search = request.GET.get("search")
    if category:
        furniture_list = furniture_list.filter(category__slug=category)
    if search:
        furniture_list = furniture_list.filter(name__icontains=search)
    return render(
        request,
        "shop/product_list.html",
        {"furniture_list": furniture_list, "categories": categories},
    )


def product_detail_view(request, slug):
    """Show details for a specific furniture item."""
    product = get_object_or_404(Furniture, slug=slug)
    return render(request, "shop/product_detail.html", {"product": product})


@login_required
def create_order_view(request, slug):
    """
    Example view to create an order for the current user.
    If you have a cart system, you'd do it differently, but this is a minimal approach.
    """
    product = get_object_or_404(Furniture, slug=slug)

    # Example: user can define quantity from a form, or we just set it to 1
    if product.stock > 0 and not product.is_sold:
        new_order = Order.objects.create(
            buyer=request.user, furniture=product, quantity=request.POST.get("quantity")
        )
        # Decrease stock
        product.stock -= 1
        product.save()
        # If stock is now 0, mark as sold
        if product.stock == 0:
            product.is_sold = True
            product.save()
        return redirect("product_detail", slug=product.slug)
    else:
        return redirect("product_list")
