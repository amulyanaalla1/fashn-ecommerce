from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Wishlist
from django.db.models import Q


def home(request):
    products = Product.objects.filter(available=True)[:8]
    return render(request, "home.html", {"products": products})

def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # CATEGORY FILTER
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # SUBCATEGORY FILTER
    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)

    # SEARCH
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # PRICE FILTER
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if min_price or max_price:
        products = products.order_by('price')

    # SORTING
    sort = request.GET.get('sort')

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "newest":
        products = products.order_by("-created")

    return render(request, 'product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })



def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    wishlist_products = []
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product', flat=True)

    return render(request, "product_detail.html", {
        "product": product,
        "wishlist_products": wishlist_products
    })


@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect("wishlist")


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})


@login_required
def remove_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect("wishlist")