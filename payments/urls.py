from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('customer_pay/<str:pk>', views.customer_pay, name='customer_pay'),
    path('supplier_pay/<str:pk>', views.supplier_pay, name='supplier_pay'),
    path('customer_paylist', views.customer_paylist, name='customer_paylist'),
    path('supplier_paylist', views.supplier_paylist, name='supplier_paylist'),
    path('create_supplier_cheque/<str:pk>', views.create_supplier_cheque, name='create_supplier_cheque'),
    path('create_customer_cheque/<str:pk>', views.create_customer_cheque, name='create_customer_cheque'),

    # API
    path('api/delivery_customer_pay/', views.ApiDeliveryCustomerPay.as_view(), name='delivery_customer_pay'),

]
