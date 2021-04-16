from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('add_supplier', views.add_supplier, name='add_supplier'),
    path('add_supplier_buyorder/<str:pk>', views.add_supplier_buyorder, name='add_supplier_buyorder'),
    path('supplier_list', views.supplier_list, name='supplier_list'),
    path('update_supplier/<str:pk>', views.update_supplier, name='update_supplier'),
    path('delete_supplier/<str:pk>', views.delete_supplier, name='delete_supplier'),

    path('buyorder_supplier_list', views.buyorder_supplier_list, name='buyorder_supplier_list'),

]
