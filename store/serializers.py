from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Order, OrderItem, Product, ProductCategory


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'group']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'group': {'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        group = Group.objects.get(name=validated_data.pop('group'))
        user = User.objects.create_user(**validated_data)
        user.groups.add(group)
        return user


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ProductCategory.objects.all()
    )

    class Meta:
        model = Product
        fields = '__all__'
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Positive number required')
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ProductCategory.objects.all()
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']

    def create(self, validated_data):
        validated_data['thumbnail'] = Product.create_thumbnail(validated_data['image'])
        return super().create(validated_data)
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Positive number required')
        return value


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Positive number required')
        return value


class OrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_surname = serializers.CharField(max_length=100)
    delivery_address = serializers.CharField(max_length=200)
    products = OrderItemSerializer(many=True)

    def save(self):
        first_name = self.data['customer_name']
        last_name = self.data['customer_surname']
        delivery_address = self.data['delivery_address']

        customer = User.objects.filter(first_name=first_name, last_name=last_name).first()

        order = Order(
            customer=customer,
            deilvery_address=delivery_address,
            order_date=datetime.now(),
            payment_date=datetime.now() + timedelta(days=5)
        )

        order_items = []
        total_price = 0
        for item in self.data['products']:
            product = Product.objects.filter(id=item['product']).first()
            order_item = OrderItem(order=order, product=product, quantity=item['quantity'])
            order_items.append(order_item)
            total_price += order_item.subtotal()

        order.total_price = total_price
        order.save()
        OrderItem.objects.bulk_create(order_items)
        return order

    def validate(self, data):
        first_name = data.get('customer_name')
        last_name = data.get('customer_surname')
        user_exists = User.objects.filter(first_name=first_name, last_name=last_name).exists()
        if not user_exists:
            raise serializers.ValidationError(
                "No user found with the provided 'customer_name' name and 'customer_surname.")
        return data
