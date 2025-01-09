from django.urls import path
from .views import home_view, product_list_view, product_detail_view, create_order_view


app_name = "furniture"

urlpatterns = [
    path("", home_view, name="home"),
    path("products/", product_list_view, name="product_list"),
    path("product/<slug:slug>/", product_detail_view, name="product_detail"),
    path("product/<slug:slug>/order/", create_order_view, name="create_order"),
]
