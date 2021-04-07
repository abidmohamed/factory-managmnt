from django.urls import path
from . import views

app_name = 'billingorder'

urlpatterns = [

    path('create_orderbill/<str:pk>', views.create_orderbill, name='create_orderbill'),
    path('bill_list', views.bill_list, name='bill_list'),
    path('bill_pdf/<str:pk>', views.bill_pdf, name='bill_pdf'),

    path('buybill_list', views.buybill_list, name='buybill_list'),
    path('buybill_pdf/<str:pk>', views.buybill_pdf, name='buybill_pdf'),
]
