from django.contrib import admin

from .models import Product, ProductCategory, Order, OrderItem


admin.site.register([Product, ProductCategory, Order, OrderItem])
