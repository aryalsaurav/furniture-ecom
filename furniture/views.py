# shop/views.py

import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse

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
    product = get_object_or_404(Furniture, slug=slug)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        # Validate quantity
        if quantity > product.stock:
            return redirect("furniture:product_detail", slug=slug)

        # Create order logic here
        total_price = product.price * quantity
        order = Order.objects.create(
            furniture=product,
            buyer=request.user,
            quantity=quantity,
            total_price=total_price,
        )

        # Update product stock
        product.stock -= quantity
        if product.stock == 0:
            product.is_sold = True
        product.save()

        return redirect("furniture:order_payment", order_id=order.pk)

    return redirect("furniture:product_detail", slug=slug)


@login_required
def order_payment_view(request, order_id):
    """
    Show a page with Khalti's payment button or popup script.
    """
    order = get_object_or_404(Order, pk=order_id)

    # The amount to Khalti must be in paisa. For example, Rs. 100 => 10000 paisa.
    amount_in_paisa = int(order.total_price * 100)

    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps(
        {
            "return_url": "http://127.0.0.1:8000/order/khalti-verify/",
            "website_url": "http://127.0.0.1:8000/",
            "amount": amount_in_paisa,
            "purchase_order_id": order.pk,
            "purchase_order_name": "test",
            "customer_info": {
                "name": order.buyer.username,
                "email": order.buyer.email,
                "phone": "9800000001",
            },
        }
    )
    headers = {
        "Authorization": "key live_secret_key_68791341fdd94846a146f0457ff7b455",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    return redirect(new_res["payment_url"])


def khalti_verify_view(request):
    """
    Khalti redirects back to this URL after payment attempt.
    We verify the payment with Khalti using the token appended to the return_url.
    """
    # Retrieve query parameters from Khalti's redirect
    purchase_order_id = int(request.GET.get("purchase_order_id"))

    # TODO: Validate these parameters as needed.
    # e.g., check if token or purchase_order_id is missing, handle error

    # Attempt to retrieve the associated order from your database
    # NOTE: In your order_payment_view, you used "purchase_order_id": "Order01"
    #       In real usage, you'd pass the actual order.pk or a unique identifier.
    order = get_object_or_404(Order, pk=purchase_order_id)
    order.paid = True
    order.save()

    return redirect("furniture:order_list")


def order_list_page(request):
    try:
        orders = Order.objects.filter(buyer=request.user)
    except:
        orders = Order.objects.all()
    return render(request, "shop/order_list.html", {"orders": orders})


@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, buyer=request.user, status="paid")
    return render(request, "furniture/order_confirmation.html", {"order": order})
