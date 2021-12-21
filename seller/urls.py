from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    # Seller
    path('add_seller/', views.add_seller, name='add_seller'),
    path('list_seller/', views.list_seller, name='list_seller'),
    path('update_seller/<str:pk>', views.update_seller, name='update_seller'),

    # Seller Stock
    path('seller_stock_list/<str:pk>', views.seller_stock_list, name='seller_stock_list'),

    # Sell Order
    path('seller_sellorder_list/<str:pk>', views.seller_sellorder_list, name='seller_sellorder_list'),
    path('seller_sellorder_details/<str:pk>', views.seller_sellorder_details, name='seller_sellorder_details'),

    # Buy Order
    path('create_seller_buyorder/<str:pk>', views.create_seller_buyorder, name='create_seller_buyorder'),
    path('seller_buyorder_confirmation/<str:pk>', views.seller_buyorder_confirmation, name='seller_buyorder_confirmation'),
    path('seller_buyorder_list', views.seller_buyorder_list, name='seller_buyorder_list'),
    path('seller_buyorder_detail/<str:pk>', views.seller_buyorder_detail, name='seller_buyorder_detail'),

    # API urls
    # path('api/listorder', views.Listorder.as_view(), name='listorder'),
    # sell order
    path('api/sell_order/', views.SellOrderList.as_view(), name='sell_order'),
    path('api/add_sell_order/', views.AddSellOrder.as_view(), name='add_sell_order'),
    # buy order
    path('api/buy_order/', views.BuyOrderList.as_view(), name='buy_order'),
    path('api/add_buy_order/', views.AddBuyOrder.as_view(), name='add_buy_order'),

    # Stock Product
    path('api/stock_product/', views.SellerStockProductList.as_view(), name='stock_product'),

    # Seller Customer
    path('api/seller_customer', views.SellerCustomerList.as_view(), name='seller_customer'),
    path('api/add_seller_customer', views.AddSellerCustomer.as_view(), name='add_seller_customer'),

]
