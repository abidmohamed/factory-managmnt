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

    # API urls
    path('api/listorder', views.Listorder.as_view(), name='listorder'),
    path('api/customer_listorder', views.ListCustomerOrder.as_view(), name='customer_listorder'),
    path('api/add_order', views.AddSellOrder.as_view(), name='add_order'),
    path('api/update_order_delivery_paid_state/<int:pk>', views.UpdatedOrderPayDeliveryState.as_view(),
         name='update_order_delivery_paid_state'),

]

