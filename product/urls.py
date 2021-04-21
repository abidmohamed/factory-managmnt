from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('all_product_list/', views.all_product_list, name='all_product_list'),
    path('product_list/<str:pk>', views.product_list, name='product_list'),
    path('add_product', views.add_product, name='add_product'),
    path('add_product_buyorder/<str:pk>', views.add_product_buyorder, name='add_product_buyorder'),
    path('update_product/<str:pk>', views.update_product, name='update_product'),
    path('product_details/<str:pk>', views.product_details, name='product_details'),
    path('delete_product/<str:pk>', views.delete_product, name='delete_product'),

    path('add_product_type/<str:pk>', views.add_type, name='add_product_type'),
    path('update_type/<str:pk>', views.update_type, name='update_type'),

]
