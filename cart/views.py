from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from accounts.models import Address

@login_required
def cart_detail(request):
    cart = request.session.get("cart", {})
    total = 0

    for item in cart.values():
        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]

    return render(request, "cart.html", {
        "cart": cart,
        "total": total
    })

def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    size = request.POST.get("size")

    cart = request.session.get("cart", {})

    key = f"{product_id}_{size}"

    if key in cart:
        cart[key]["quantity"] += 1
    else:
        cart[key] = {
            "name": product.name,
            "price": float(product.price),
            "image":product.image.url,
            "size": size,
            "quantity": 1
        }

    request.session["cart"] = cart

    return redirect("cart_detail")

def remove_cart(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        del cart[key]

    request.session["cart"] = cart
    return redirect("cart_detail")


def order_success(request):
    return render(request, "order_success.html")


def increase_quantity(request, key):

    cart = request.session.get("cart", {})

    if key in cart:
        cart[key]["quantity"] += 1

    request.session["cart"] = cart

    return redirect("cart_detail")


def decrease_quantity(request, key):

    cart = request.session.get("cart", {})

    if key in cart:

        cart[key]["quantity"] -= 1

        if cart[key]["quantity"] <= 0:
            del cart[key]

    request.session["cart"] = cart

    return redirect("cart_detail")




