from django.urls import path
from .views import (
    home_view,
    product_list_view,
    product_detail_view,
    create_order_view,
    order_payment_view,
    khalti_verify_view,
    order_confirmation_view,
    order_list_page,
)


app_name = "furniture"

urlpatterns = [
    path("", home_view, name="home"),
    path("products/", product_list_view, name="product_list"),
    path("product/<slug:slug>/", product_detail_view, name="product_detail"),
    path("product/<slug:slug>/order/", create_order_view, name="create_order"),
    path("order/payment/<int:order_id>/", order_payment_view, name="order_payment"),
    path("order/khalti-verify/", khalti_verify_view, name="khalti_verify"),
    path(
        "order/confirmation/<int:order_id>/",
        order_confirmation_view,
        name="order_confirmation",
    ),
    path("order/list/", order_list_page, name="order_list"),
]
