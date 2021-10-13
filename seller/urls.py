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

    # API urls
    # path('api/listorder', views.Listorder.as_view(), name='listorder'),
    # sell order
    path('api/sell_order/', views.SellOrderList.as_view(), name='sell_order'),
    path('api/add_sell_order/', views.AddSellOrder.as_view(), name='add_sell_order'),
    # buy order
    path('api/buy_order/', views.BuyOrderList.as_view(), name='buy_order'),
    path('api/add_buy_order/', views.AddBuyOrder.as_view(), name='add_buy_order'),

]
