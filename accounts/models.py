from django.contrib.auth.models import AbstractUser
from django.db import models
#from accounts.models import CustomUser


class CustomUser(AbstractUser):

    phone = models.CharField(max_length=15, blank=True, null=True)

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


class Address(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=15)

    address_line = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"