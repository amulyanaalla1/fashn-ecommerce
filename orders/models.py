from django.db import models
from accounts.models import CustomUser, Address
from products.models import Product

class Order(models.Model):

    STATUS_CHOICES = (
        ("PREPARING", "Preparing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    )

    PAYMENT_CHOICES = (
        ("UPI", "UPI"),
        ("CARD", "Card / Netbanking"),
        ("COD", "Cash on Delivery"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="COD")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PREPARING")

    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    product_name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField()

    size = models.CharField(max_length=10)

    image = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.product_name