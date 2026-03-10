from django.urls import path
from . import views

urlpatterns = [

    # product list
    path("", views.product_list, name="product_list"),

    # wishlist
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/", views.remove_wishlist, name="remove_wishlist"),

    # product detail
    path("products/item/<slug:slug>/", views.product_detail, name="product_detail"),

    # category filter 
    path("<slug:category_slug>/", views.product_list, name="products_by_category"),

]