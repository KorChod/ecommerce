from django.urls import path

from .views import OrderView, ProductList, ProductDetail,  ProductStatisticsView, \
    UserRegistrationView


urlpatterns = [
    path('users/register/', UserRegistrationView.as_view()),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    path('orders/', OrderView.as_view()),
    path('statistics/products/', ProductStatisticsView.as_view()),
]
