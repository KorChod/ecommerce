from datetime import datetime

from django.db import transaction
from django.db.models import Sum, F
from django.core.mail import send_mail
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Order, OrderItem, Product
from .permissions import IsAuthenticatedSeller, \
    IsAuthenticatedCustomerOrReadonly, \
    IsAuthenticatedSellerOrReadonly
from .serializers import OrderSerializer, ProductSerializer, ProductCreateSerializer, UserSerializer


class UserRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductList(ListCreateAPIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [IsAuthenticatedSellerOrReadonly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ['name', 'category', 'price']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        else:
            return ProductSerializer


class ProductDetail(APIView):
    serializer_class = ProductSerializer
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [IsAuthenticatedSellerOrReadonly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [IsAuthenticatedCustomerOrReadonly]
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()
        user_email = request.user.email
        if user_email:
            send_mail(
                "Order received",
                "We'd like to let you know that your order has been received.",
                "dummy@ecommerce.com",
                [user_email],
                fail_silently=False,
            )
        response = {"payment_date": order.payment_date, "total_price": order.total_price}
        return Response(response)


class ProductStatisticsView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [IsAuthenticatedSeller]

    def get(self, request, format=None):
        date_format = "%Y-%m-%d"
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')
        products_number = request.GET.get('products-number')

        query_filters = {}

        if date_from and self.__is_valid_date(date_from, date_format):
            query_filters['order_date__gte'] = datetime.strptime(date_from, date_format)

        if date_to and self.__is_valid_date(date_to, date_format):
            query_filters['order_date__lt'] = datetime.strptime(date_to, date_format)

        orders = Order.objects.filter(**query_filters)

        product_data = (
            OrderItem.objects
            .filter(order__in=orders)
            .values(product_name=F('product__name'))
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
        )

        if products_number and self.__is_integer(products_number):
            product_data = product_data[:int(products_number)]
        return Response(product_data)

    def __is_valid_date(self, date_string, date_format):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def __is_integer(self, input_string):
        try:
            int(input_string)
            return True
        except ValueError:
            return False
