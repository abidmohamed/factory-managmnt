from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('created/', views.order_create, name='order_create'),
    path('order_pdf/<str:pk>', views.order_pdf, name='order_pdf'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_list_by_city/<str:pk>', views.order_list_by_city, name='order_list_by_city'),
    path('order_confirmation/<str:pk>', views.order_confirmation, name='order_confirmation'),
    path('sellorder_details/<str:pk>', views.sellorder_details, name='sellorder_details'),
    path('order_delivered/<str:pk>', views.order_delivered, name='order_delivered'),

]

