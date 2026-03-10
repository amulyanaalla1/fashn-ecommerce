from django.db import models
from django.urls import reverse
from django.conf import settings

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


SIZE_CHOICES = [
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='products/')

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        blank=True,
        null=True
    )

    available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.name


# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')
#     available = models.BooleanField(default=True)

#     def get_absolute_url(self):
#         return reverse('product_detail', args=[self.slug])

#     def __str__(self):
#         return self.name
