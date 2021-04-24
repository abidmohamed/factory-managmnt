from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from billingorder.models import OrderBilling, BillOrderItem
from cart.cart import Cart
from customer.models import Customer, City
from accounts.decorators import customer_only, admin_only
from order.models import Order, OrderItem
from product.models import ProductType
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
                    # Get the stock to take values from
                    stockitem = StockProduct.objects.get(product=orderitem.product,
                                                         type=orderitem.product_type,
                                                         )
                    print(stockitem)
                    if stockitem is not None:
                        if stockitem.quantity < int(orderitem.quantity):
                            currentorder.factured = False
                            currentorder.save()
                            return HttpResponse('We had some errors <pre>Not Enough Quantity</pre>')
                        else:
                            stockitem.quantity -= int(orderitem.quantity)
                            stockitem.save()

                    # stockproduct = StockProduct.objects.get(id=orderitem.stockproduct.id)
                    # stockproduct.quantity = stockproduct.quantity - orderitem.quantity
                    # stockproduct.save()

            pk = orderbilling.id
            return redirect(f"../../billingorder/create_orderbill/{pk}")

    context = {'orders': orders}
    return render(request, 'order/billing_list_order.html', context)

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
