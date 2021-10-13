import decimal

from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from customer.forms import UserForm
from customer.models import Customer
from product.models import Product, ProductType
from seller.forms import SellerForm
from seller.models import Seller, SellerSellOrder, SellerBuyOrder, OrderItem, BuyOrderItem, SellerStock, \
    SellerStockProduct
from seller.serializers import SellerSerializer, SellerSellOrderSerializer, SellerBuyOrderSerializer, \
    AddSellerSellOrderSerializer, AddSellerBuyOrderSerializer
from warehouse.models import Stock, StockProduct


# SELLER
def add_seller(request):
    user_form = UserForm()
    seller_form = SellerForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        seller_form = SellerForm(request.POST)

        if seller_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            seller = seller_form.save(commit=False)
            # check if seller group exists
            if Group.objects.all().filter(name='seller'):
                group = Group.objects.get(name='seller')
            else:
                group = Group.objects.create(name='seller')

            user.groups.add(group)

            seller.user = user
            seller.save()
            stock_name = user.first_name + " " + user.last_name + " stock"
            SellerStock.objects.create(seller=seller, name=stock_name)
            return redirect('seller:list_seller')
    context = {
        'user_form': user_form,
        'seller_form': seller_form
    }

    return render(request, 'seller/add.html', context)


def list_seller(request):
    sellers = Seller.objects.all()
    context = {
        'sellers': sellers,
    }
    return render(request, 'seller/list.html', context)


def update_seller(request, pk):
    seller = get_object_or_404(Seller, id=pk)
    user = get_object_or_404(User, id=seller.user.id)

    seller_form = SellerForm(instance=seller)
    user_form = UserForm(instance=user)

    if request.method == 'POST':
        seller_form = SellerForm(request.POST, instance=seller)
        user_form = UserForm(request.POST, instance=user)

        if seller_form.is_valid():
            updated_user = user_form.save()
            updated_seller = seller_form.save(commit=False)
            updated_seller.user = updated_user
            updated_seller.save()
            return redirect('seller:list_seller')
    context = {
        'user_form': user_form,
        'seller_form': seller_form
    }

    return render(request, 'seller/add.html', context)


# SELLER STOCK
def seller_stock_list(request, pk):
    seller = get_object_or_404(Seller, id=pk)
    stock = get_object_or_404(SellerStock, seller=seller)

    stock_products = SellerStockProduct.objects.filter(stock=stock, quantity__gt=0)
    total_sell_price1 = 0
    total_sell_price2 = 0
    total_sell_price3 = 0
    total_sell_price4 = 0
    total_sell_price5 = 0
    total_sell_price6 = 0
    total_buy_price = 0
    for item in stock_products:
        total_sell_price1 += item.product_type.price1
        total_sell_price2 += item.product_type.price2
        total_sell_price3 += item.product_type.price3
        total_sell_price4 += item.product_type.price4
        total_sell_price5 += item.product_type.price5
        total_sell_price6 += item.product_type.price6
        total_buy_price += item.product_type.buyprice

    context = {
        'stock_products': stock_products,
        'seller': seller, 'total_sell_price1': total_sell_price1,
        'total_sell_price2': total_sell_price2, 'total_sell_price3': total_sell_price3,
        'total_sell_price4': total_sell_price4, 'total_sell_price5': total_sell_price5,
        'total_sell_price6': total_sell_price6, 'total_buy_price': total_buy_price,

    }

    return render(request, 'stock/list.html', context)


# SELLER SELL ORDER
def seller_sellorder_list(request, pk):
    seller = get_object_or_404(Seller, id=pk)
    orders = SellerSellOrder.objects.filter(user=seller.user.id)
    print(orders)

    context = {
        "orders": orders,
    }
    return render(request, "sellorder/list.html", context)

"""
###################################API Classes 
"""


class ListSeller(ListAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()


# Sell Order
class SellOrderList(ListAPIView):
    serializer_class = SellerSellOrderSerializer
    queryset = SellerSellOrder.objects.all()


class AddSellOrder(CreateAPIView):
    serializer_class = AddSellerSellOrderSerializer

    def create(self, request, *args, **kwargs):
        print("##############DATA###############>", request.data)
        if request.method == 'POST':
            serializer = AddSellerSellOrderSerializer(data=request.data)

            if serializer.is_valid():
                totalorderprice = decimal.Decimal('0.0')
                index = 0
                # Get order items
                order_items = request.data['selleritems']
                # Get seller
                if Seller.objects.filter(user=request.user):
                    # Order customer
                    customer = Customer.objects.get(id=request.data['customer'])
                    isPaid = request.data['paid']
                    print(customer)
                    # Saving order
                    order = SellerSellOrder.objects.create(customer=customer, paid=isPaid, user=request.user.id)
                    seller = Seller.objects.get(user=request.user)
                    # Calculate total order price
                    while index < len(order_items):
                        # get product
                        product = Product.objects.get(id=order_items[index]['product'])
                        # print(product)
                        # get product type
                        product_type = ProductType.objects.get(id=order_items[index]['product_type'], product=product)
                        # Item price & weight & quantity
                        item_price = decimal.Decimal(order_items[index]['price'])
                        weight = order_items[index]['weight']
                        quantity = order_items[index]['quantity']
                        # Saving Seller Sell Order Items
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_type=product_type,
                            price=item_price,
                            weight=weight,
                            quantity=quantity,
                        )
                        # get Price
                        totalorderprice += item_price
                        # UPDATE SELLER STOCK
                        sellerstock = SellerStock.objects.get(seller=seller)
                        sellerstock_product = SellerStockProduct.objects.get(
                            product=product,
                            product_type=product_type,
                            stock=sellerstock
                        )
                        sellerstock_product.quantity -= quantity
                        sellerstock_product.save()

                        index += 1

                    print("Total Price ", totalorderprice)
                    # customer debt & seller in hold money
                    customer.debt += totalorderprice
                    seller.in_hold_money += totalorderprice

                    customer.save()
                    seller.save()
                else:
                    print("Not Seller")
                    return Response({"Not Authorized": request.data}, status=status.HTTP_403_FORBIDDEN)

                # print("Products ====>", products)

                # serializer.save(user=self.request.user.id)
                return Response({"Success": request.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"Bad Request": request.data}, status=status.HTTP_400_BAD_REQUEST)


# Buy Order
class BuyOrderList(ListAPIView):
    serializer_class = SellerBuyOrderSerializer
    queryset = SellerBuyOrder.objects.all()


class AddBuyOrder(CreateAPIView):
    serializer_class = AddSellerBuyOrderSerializer

    def create(self, request, *args, **kwargs):
        print("##############DATA###############>", request.data)
        if request.method == 'POST':
            serializer = AddSellerBuyOrderSerializer(data=request.data)

            if serializer.is_valid():
                totalorderprice = decimal.Decimal('0.0')
                index = 0
                # get order items
                order_items = request.data['selleritems']
                # Get seller
                seller = Seller.objects.get(id=request.data['seller'])
                isPaid = request.data['paid']
                # get user
                user = request.user
                # Saving Order
                order = SellerBuyOrder.objects.create(seller=seller, paid=isPaid, user=user.id)
                # calculate order total price
                while index < len(order_items):
                    # get product & product type & stock
                    product = Product.objects.get(id=order_items[index]['product'])
                    # print(product)
                    # get product type
                    product_type = ProductType.objects.get(id=order_items[index]['product_type'], product=product)
                    stock = Stock.objects.get(id=order_items[index]['stock'])
                    # Get price & quantity
                    item_price = decimal.Decimal(order_items[index]['price'])
                    quantity = order_items[index]['quantity']
                    # Saving Seller Buy Order Item
                    BuyOrderItem.objects.create(
                        order=order,
                        product=product,
                        product_type=product_type,
                        price=item_price,
                        quantity=quantity,
                        stock=stock,
                    )

                    # Update stock values
                    # Get seller stock
                    sellerstock = SellerStock.objects.get(seller=seller)
                    itemexist = 1
                    if SellerStockProduct.objects.filter(stock=sellerstock):
                        # stock is not empty
                        print("Stock Not Empty")
                        sellerstock_products = SellerStockProduct.objects.all().filter(stock=sellerstock)
                        for seller_stock_product in sellerstock_products:
                            print("Seller Stock Product ==>", seller_stock_product)
                            print(" Product ==>", product)

                            if product == seller_stock_product.product and \
                                    product_type == seller_stock_product.product_type:
                                # Product Already exist
                                print("Product Exists Already")
                                seller_stock_product.quantity += quantity
                                seller_stock_product.save()
                                stock_product = StockProduct.objects.get(product=product, stock=stock,
                                                                         type=product_type)
                                stock_product.quantity -= quantity
                                stock_product.save()
                                itemexist = 2
                                break
                        if itemexist == 1:
                            # Product does not exist
                            print("Product Does Not Exist Already")
                            SellerStockProduct.objects.create(
                                product=product,
                                quantity=quantity,
                                category=product.category,
                                stock=sellerstock,
                                product_type=product_type,
                            )
                            # update general stock
                            stock_product = StockProduct.objects.get(product=product, stock=stock, type=product_type)
                            stock_product.quantity -= quantity
                            stock_product.save()
                    else:
                        # stock is empry
                        print("Stock is Empty")
                        SellerStockProduct.objects.create(
                            product=product,
                            quantity=quantity,
                            category=product.category,
                            stock=sellerstock,
                            product_type=product_type,
                        )
                        # update general stock
                        stock_product = StockProduct.objects.get(product=product, stock=stock, type=product_type)
                        stock_product.quantity -= quantity
                        stock_product.save()

                    # get Total Price
                    totalorderprice += item_price
                    index += 1

                seller.debt += totalorderprice
                seller.save()

                return Response({"Success": request.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"Bad Request": request.data}, status=status.HTTP_400_BAD_REQUEST)
