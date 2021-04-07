from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('add_delivery', views.add_delivery, name='add_delivery'),
    path('delivery_list', views.delivery_list, name='delivery_list'),
    path('update_delivery/<str:pk>', views.update_delivery, name='update_delivery'),
    path('delete_delivery/<str:pk>', views.delete_delivery, name='delete_delivery'),


]
