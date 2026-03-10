from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/',views.account_page,name='account_page'),
    path('add_address/',views.add_address,name='add_address'),
    path("delete-address/<int:address_id>/", views.delete_address, name="delete_address"),
]