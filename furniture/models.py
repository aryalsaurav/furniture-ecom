from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug and self.name:
            self.slug = slugify(self.name) + "-" + str(self.pk or "")
        super().save(*args, **kwargs)


class Furniture(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="furniture"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="furniture_images/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    is_sold = models.BooleanField(default=False)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug and self.name:
            self.slug = slugify(self.name) + "-" + str(self.pk or "")
        super().save(*args, **kwargs)


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Order #{self.pk} by {self.buyer.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.furniture.price * self.quantity
        super().save(*args, **kwargs)
