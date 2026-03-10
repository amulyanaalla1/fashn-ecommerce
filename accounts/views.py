from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from orders.models import Order,Address
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import get_object_or_404

User = get_user_model()

def signup(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # authenticate user before login
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

        return redirect("home")

    return render(request, "accounts/signup.html")

@login_required
def account_page(request):

    user = request.user
    addresses=Address.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by("-created")

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("account_page")

    else:
        form = ProfileForm(instance=user)

    return render(request, "accounts/account.html", {
        "form": form,
        "orders": orders,
        "addresses":addresses
    })

def add_address(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address_line = request.POST.get("street")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            city=city,
            pincode=pincode
        )

        return redirect("account_page")

    return render(request, "accounts/add_address.html")


def delete_address(request, address_id):

    address = get_object_or_404(Address, id=address_id, user=request.user)

    address.delete()

    return redirect("account_page")

