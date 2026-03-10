from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<str:key>/", views.remove_cart, name="remove_cart"),
    path("success/", views.order_success, name="order_success"),
    path("increase/<str:key>/", views.increase_quantity, name="increase_quantity"),

    path("decrease/<str:key>/", views.decrease_quantity, name="decrease_quantity"),
]