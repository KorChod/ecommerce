from django_filters.rest_framework import CharFilter, FilterSet

from .models import Product


class ProductFilter(FilterSet):
    category = CharFilter(field_name='category__name', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price']
