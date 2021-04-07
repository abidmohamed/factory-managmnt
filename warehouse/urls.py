from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [

    # path('add_warehouse', views.add_warehouse, name='add_warehouse'),
    # path('warehouse_list', views.warehouse_list, name='warehouse_list'),
    # path('update_warehouse/<str:pk>', views.update_warehouse, name='update_warehouse'),
    # path('delete_warehouse/<str:pk>', views.delete_warehouse, name='delete_warehouse'),

    path('add_stock', views.add_stock, name='add_stock'),
    path('stock_list/<str:pk>', views.stock_list, name='stock_list'),
    path('all_stock_list', views.all_stock_list, name='all_stock_list'),
    path('update_stock/<str:pk>', views.update_stock, name='update_stock'),
    path('delete_stock/<str:pk>', views.delete_stock, name='delete_stock'),

    path('add_stockproduct', views.add_stockproduct, name='add_stockproduct'),
    path('stockproduct_list/<str:pk>', views.stockproduct_list, name='stockproduct_list'),
    path('all_stockproduct_list', views.all_stockproduct_list, name='all_stockproduct_list'),
    path('update_stockproduct/<str:pk>', views.update_stockproduct, name='update_stockproduct'),
    path('delete_stockproduct/<str:pk>', views.delete_stockproduct, name='delete_stockproduct'),
    path('stockproductcategory_list/<str:pk>', views.stockproductcategory_list, name='stockproductcategory_list'),
    path('stockproduct_detail/<str:id>', views.stockproduct_detail, name='stockproduct_detail'),
    path('stockproduct_stockalert', views.stockproduct_quantityalert, name='stockproduct_stockalert'),

    # path('autocomplete_product', views.productautocomplete, name='autocomplete_product'),
    path('autocomplete_product', views.CompleteProduct.as_view, name='autocomplete_product'),
    path('ajax/load-types/', views.loadtypes, name='ajax_load_types'),
    path('ajax/load-price/', views.loadprice, name='ajax_load_price'),

]
