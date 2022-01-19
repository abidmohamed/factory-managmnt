import decimal
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from xhtml2pdf import pisa

from billingorder.models import OrderBilling, BillOrderItem
from cart.cart import Cart
from customer.models import Customer, City
from accounts.decorators import customer_only, admin_only
from delivery.models import Delivery
from order.models import Order, OrderItem
from order.serializers import SellOrderSerializer, AddSellOrderSerializer
from product.models import ProductType, Product
from warehouse.models import StockProduct, Stock


def order_pdf(request, pk):
    order = get_object_or_404(Order, id=pk)
    html = render_to_string('order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}_{order.customer}_{order.created}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@customer_only
def order_create(request):
    customer = Customer.objects.get(user=request.user)
    cart = Cart(request)
    # print(cart)
    for item in cart:
        st = item['product_type'].id
        print(st)
    if request.method == 'POST':
        order = Order()
        order.customer = customer
        order.save()
        for item in cart:
            # print(item)
            # stockproduct = StockProduct.objects.get(id=item['stockproduct'].id)
            # stockproduct.quantity = stockproduct.quantity - item['quantity']
            # stockproduct.save()
            product_type = ProductType.objects.get(id=item['product_type'].id)
            OrderItem.objects.create(order=order,
                                     product=product_type.product,
                                     product_type=product_type,
                                     price=item['price'],
                                     weight=product_type.weight,
                                     quantity=item['quantity'])
        if customer.debt is not None:
            customer.debt += order.get_total_cost()
        else:
            customer.debt = order.get_total_cost()
        customer.save()
        # clear the cart
        cart.clear()
        return redirect(f'../order_pdf/{order.pk}')

    context = {
        'cart': cart
    }
    return render(request, 'order/create.html', context)


def sellorder_details(request, pk):
    order = Order.objects.get(id=pk)
    context = {
        'order': order
    }
    return render(request, 'order/sellorder_details.html', context)


@admin_only
def order_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}

    return render(request, 'order/list_order.html', context)


@admin_only
def order_list_by_city(request, pk):
    city = City.objects.get(id=pk)
    # get customer from the chosen city
    customers = Customer.objects.all().filter(city=city)
    orders = Order.objects.none()
    for customer in customers:
        # print(customer)
        # get orders of the chosen customers from the chosen city above
        orders |= Order.objects.all().filter(customer=customer, factured=False)
    # print(orders)
    if request.method == 'POST':
        # get submitted orders
        chosenorders = request.POST.getlist("orders")
        # create billing object if there is selected orders
        if len(chosenorders) != 0:
            orderbilling = OrderBilling()
            orderbilling.user = request.user.id
            orderbilling.save()
            for orderid in chosenorders:
                currentorder = Order.objects.get(id=orderid)
                currentorder.factured = True
                currentorder.save()
                orderprice = currentorder.get_total_cost()
                orderweight = currentorder.get_total_weight()
                print(orderweight)
                BillOrderItem.objects.create(
                    bill=orderbilling,
                    order=currentorder,
                    price=orderprice,
                    weight=orderweight,
                )

                # reduce quantity from the stock
                currentorderitems = currentorder.items.all()
                for orderitem in currentorderitems:
                    print(orderitem)
                    # Get the stock to take values from if product exists
                    if StockProduct.objects.filter(product=orderitem.product, type=orderitem.product_type):
                        stockitems = StockProduct.objects.filter(product=orderitem.product,
                                                                 type=orderitem.product_type,
                                                                 )
                        for stockitem in stockitems:
                            print(stockitem)
                            if stockitem is not None:
                                # if stockitem.quantity < int(orderitem.quantity):
                                #     currentorder.factured = False
                                #     currentorder.save()
                                #     return HttpResponse('We had some errors <pre>Not Enough Quantity</pre>')
                                # else:
                                stockitem.quantity -= int(orderitem.quantity)
                                stockitem.save()

                    else:
                        currentorder.factured = False
                        currentorder.save()
                        orderprice = currentorder.get_total_cost()
                        orderweight = currentorder.get_total_weight()
                        print(orderweight)
                        BillOrderItem.objects.get(order=currentorder, )
                        BillOrderItem.delete()
                        return HttpResponse('We had some errors <pre>Product not available in Stock</pre>')

                    # stockproduct = StockProduct.objects.get(id=orderitem.stockproduct.id)
                    # stockproduct.quantity = stockproduct.quantity - orderitem.quantity
                    # stockproduct.save()

            pk = orderbilling.id
            return redirect(f"../../billingorder/create_orderbill/{pk}")
    context = {'orders': orders}
    return render(request, 'order/billing_list_order.html', context)


@admin_only
def order_confirmation(request, pk):
    sellorder = Order.objects.get(id=pk)
    if request.method == 'POST':
        # submitted values
        prices = request.POST.getlist('prices')
        quantities = request.POST.getlist('quantities')
        chosen_date = request.POST.get('order_date')
        # get year month day
        chosen_year = chosen_date.split("-", 1)
        chosen_month = chosen_date.split("-", 2)
        chosen_day = chosen_date.split("-", 2)

        # change each item values
        if sellorder.items.all():
            for index, item in enumerate(sellorder.items.all()):
                # get the price and value of each element
                # Saving the orderitem
                str_price = prices[index]
                str_price = str_price.replace(",", ".")
                # str_price = str_price.replace(' ', '')
                # Remove white spaces
                str_price = ''.join(str_price.split())
                item.price = str_price
                item.quantity = quantities[index]
                item.save()
        sellorder.order_date = date(int(chosen_year[0]), int(chosen_month[1]), int(chosen_day[2]))
        sellorder.save()
        return redirect('order:order_list')
    context = {
        'sellorder': sellorder,
    }

    return render(request, 'order/order_confirmation.html', context)


# def render_pdf_view(request):
#     template_path = 'user_printer.html'
#     context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#
#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

# Order Deliver
def order_delivered(request, pk):
    # get the order
    order = get_object_or_404(Order, id=pk)
    # Add Money to delivery man
    delivery = get_object_or_404(Delivery, user=request.user)
    # delivery.money += order.get_total_cost()
    # set order to delivered
    order.delivered = True
    delivery.save()
    order.save()

    return redirect('payments:delivery_customer_pay', order.id)


# =========> API's View
# Sell Order
class Listorder(ListAPIView):
    serializer_class = SellOrderSerializer
    queryset = Order.objects.filter(delivered=False)


# Add Sell Order
class AddSellOrder(CreateAPIView):
    serializer_class = AddSellOrderSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = AddSellOrderSerializer(data=request.data)

            if serializer.is_valid():
                totalorderprice = decimal.Decimal('0.0')
                index = 0
                # Get Order Items
                order_items = request.data['items']
                # Get Customer
                # if Customer.objects.filter(user=request.user):
                # Order customer
                customer = Customer.objects.get(id=request.data['customer'])
                isPaid = request.data['paid']
                isDelivered = request.data['delivered']
                # saving order
                order = Order.objects.create(customer=customer, paid=isPaid, delivered=isDelivered,
                                             user=request.user)
                # Calculate total order price
                while index < len(order_items):
                    # get product
                    product = Product.objects.get(id=order_items[index]['product'])
                    # get product type
                    product_type = ProductType.objects.get(id=order_items[index]['product_type'], product=product)
                    # Item price & weight & quantity
                    item_price = decimal.Decimal(order_items[index]['price'])
                    weight = order_items[index]['weight']
                    quantity = order_items[index]['quantity']
                    quantity = int(quantity)
                    # Saving Order Items
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

                    index += 1

                return Response({"Success": request.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Bad Request": request.data}, status=status.HTTP_400_BAD_REQUEST)

                # else:
                # not a customer
                # return Response({"Not Authorized": request.data}, status=status.HTTP_403_FORBIDDEN)


class UpdatedOrderPayDeliveryState(UpdateAPIView):

    def patch(self, request, pk, *args, **kwargs, ):
        data = request.data
        # print(data)
        order = get_object_or_404(Order, id=pk)
        # print(order)
        # print(order.delivered)
        order.delivered = data.get('delivered', order.delivered)
        order.paid = data.get('paid', order.paid)
        # print(order.delivered)
        order.save()

        # serializer = SellOrderSerializer(data=order)

        return Response({"data": data}, status=status.HTTP_202_ACCEPTED)
