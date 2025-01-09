from django.contrib import admin

from .models import Furniture, Category, Order

# Register your models here.
admin.site.register(Furniture)
admin.site.register(Category)
admin.site.register(Order)
