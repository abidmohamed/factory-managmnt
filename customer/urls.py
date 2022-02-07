from django.urls import path
from . import views
from .views import ListCustomerApi, DetailCustomerApi

app_name = 'customer'

urlpatterns = [
    path('add_customer', views.add_customer, name='add_customer'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('customer_detail/<str:pk>', views.customer_detail, name='customer_detail'),
    path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),

    # API
    path('api/customer_list', ListCustomerApi.as_view(), name='customer_list_api'),
    path('api/customer_detail/<str:pk>/', DetailCustomerApi.as_view(), name='customer_detail_api'),

    path('add_city', views.add_city, name='add_city'),
    path('order_city_list', views.order_city_list, name='order_city_list'),
    path('buyorder_city_list', views.buyorder_city_list, name='buyorder_city_list'),
    path('city_list', views.city_list, name='city_list'),
    path('update_city/<str:pk>', views.update_city, name='update_city'),
    path('delete_city/<str:pk>', views.delete_city, name='delete_city'),

]
