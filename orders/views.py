from django.shortcuts import render, redirect
from orders.models import Order, OrderItem
from accounts.models import Address
#import random
from products.models import Product


def checkout(request):

    cart = request.session.get("cart", {})

    # Stop if cart empty
    if not cart:
        return redirect("cart")

    addresses = Address.objects.filter(user=request.user)

    total = 0
    for item in cart.values():
        total += item["price"] * item["quantity"]

    if request.method == "POST":

        # Prevent duplicate orders
        if request.session.get("order_processing"):
            return redirect("my_orders")

        request.session["order_processing"] = True

        address_id = request.POST.get("address")
        address = Address.objects.get(id=address_id, user=request.user)

        order_items = []
        total = 0

        # Prepare items first
        for key, item in cart.items():

            product_id = key.split("_")[0]
            product = Product.objects.get(id=product_id)

            subtotal = item["price"] * item["quantity"]
            total += subtotal

            order_items.append({
                "product": product,
                "product_name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "size": item["size"],
                "image": item["image"]
            })

        # Create order once
        order = Order.objects.create(
            user=request.user,
            address=address,
            total=total
        )

        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_name=item["product_name"],
                price=item["price"],
                quantity=item["quantity"],
                size=item["size"],
                image=item["image"]
            )

        # Clear cart
        request.session["cart"] = {}

        # Unlock checkout
        if "order_processing" in request.session:
            del request.session["order_processing"]

        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "cart": cart,
        "addresses": addresses,
        "total": total
    })

def order_success(request,order_id):

    order = Order.objects.create(
        user=request.user,
        address=request.user.addresses.first(),
        total=2000,
        paid=True
    )

    return render(request,"orders/order_success.html",{"order":order})

def order_detail(request, order_id):

    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, "orders/order_detail.html", {
        "order": order
    })

def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created")

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })








