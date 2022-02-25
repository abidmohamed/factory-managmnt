from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('customer_pay/<str:pk>', views.customer_pay, name='customer_pay'),
    path('supplier_pay/<str:pk>', views.supplier_pay, name='supplier_pay'),
    path('seller_pay/<str:pk>', views.seller_pay, name='seller_pay'),

    path('customer_paylist', views.customer_paylist, name='customer_paylist'),
    path('supplier_paylist', views.supplier_paylist, name='supplier_paylist'),
    path('seller_paylist', views.seller_paylist, name='seller_paylist'),

    path('create_supplier_cheque/<str:pk>', views.create_supplier_cheque, name='create_supplier_cheque'),
    path('create_customer_cheque/<str:pk>', views.create_customer_cheque, name='create_customer_cheque'),

    # API
    path('api/delivery_customer_pay/', views.ApiDeliveryCustomerPay.as_view(), name='delivery_customer_pay'),
    path('api/customer_pay/<str:pk>', views.ApiSellerCustomerPay.as_view(), name='api_customer_pay'),
    path('api/list_customer_pay/<str:pk>', views.list_customer_pay, name='api_list_customer_pay'),

]
