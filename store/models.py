from enum import Enum
from io import BytesIO
from PIL import Image

from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.dispatch import receiver


class Role(Enum):
    SELLER = 'Seller'
    CUSTOMER = 'Customer'


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name=Role.SELLER.value)
    Group.objects.get_or_create(name=Role.CUSTOMER.value)


class ProductCategory(models.Model):
    class Meta:
        verbose_name_plural = "Product categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(unique=True, max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    thumbnail = models.ImageField(upload_to='images/', blank=False, null=False)

    def __str__(self):
        return self.name

    @classmethod
    def create_thumbnail(cls, uploaded_file):
        image_data = uploaded_file.read()

        image = Image.open(BytesIO(image_data))

        max_width = 200
        aspect_ratio = image.width / image.height
        thumbnail_width = max_width
        thumbnail_height = int(max_width / aspect_ratio)

        image.thumbnail((thumbnail_width, thumbnail_height))

        modified_image_data = BytesIO()
        image.save(modified_image_data, format='png')

        return ContentFile(modified_image_data.getvalue(), name=f'thumbnail_{uploaded_file.name}')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    deilvery_address = models.CharField(max_length=200)
    order_date = models.DateTimeField()
    payment_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order number: {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product}: {self.quantity}'
