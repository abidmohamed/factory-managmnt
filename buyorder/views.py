from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from billingorder.models import BillBuyOrderItem, BuyOrderBilling
from buyorder.forms import BuyOrderForm, BuyOrderItemFormset
from buyorder.models import BuyOrderItem, BuyOrder
from customer.models import City
from product.forms import ProductForm
from product.models import Product, ProductType
from supplier.forms import SupplierForm
from supplier.models import Supplier
from warehouse.models import StockProduct, Stock


def create_buyorder(request, pk):
    city = City.objects.get(id=pk)
    stocks = Stock.objects.all().filter(city=city)
    buyorderform = BuyOrderForm()
    productform = ProductForm()
    supplierform = SupplierForm()
    buyorderitemformset = BuyOrderItemFormset(queryset=BuyOrderItem.objects.none())

    products = Product.objects.all()

    if request.method == 'POST':
        print(request.POST)
        # fix the form to be validated
        # get the list of the chosen products
        products_list = request.POST.getlist('products')
        # print(products_list)
        buyorderform = BuyOrderForm(request.POST)
        # if the list has elements

        if buyorderform.is_valid():
            if len(products_list):
                buyorder = buyorderform.save(commit=False)
                buyorder.city = city
                buyorder.user = request.user.id
                buyorder.save()
                # to add credit
                # supplier = Supplier.objects.get(id=request.POST['supplier'])
                for index, prod_list_item in enumerate(products_list):
                    # saving the order items
                    # print(types_list[index])
                    orderitem = BuyOrderItem()
                    orderitem.order = buyorder
                    orderitem.product = Product.objects.get(id=prod_list_item)
                    orderitem.price = Product.objects.get(id=prod_list_item).buyprice
                    orderitem.save()
                    # print(Product.objects.get(id=prod_list_item))

            return redirect('buyorder:buyorder_confirmation', buyorder.pk)
    context = {
        'products': products,
        'buyorderform': buyorderform,
        'buyorderitemformset': buyorderitemformset,
        'stocks': stocks,
        'productform': productform,
        'supplierform': supplierform,
        'city': city,
    }
    return render(request, 'buyorder/add_buyorder.html', context)


def buyorder_confirmation(request, pk):
    buyorder = BuyOrder.objects.get(id=pk)
    stocks = Stock.objects.all().filter(city=buyorder.city)

    buyorderform = BuyOrderForm(instance=buyorder)
    if request.method == 'POST':
        buyorderform = BuyOrderForm(request.POST, instance=buyorder)
        if buyorderform.is_valid():
            print(request.POST)

            buyorder = buyorderform.save()
            # to add credit
            supplier = Supplier.objects.get(id=request.POST['supplier'])
            # get modified items
            prices = request.POST.getlist('prices')
            quantities = request.POST.getlist('quantities')
            types = request.POST.getlist('type')
            stocklist = request.POST.getlist('stock')
            for index, item in enumerate(buyorder.items.all()):
                # print(index, item)
                print(prices[index], quantities[index], types[index], stocklist[index])
                # get the price and value of each element
                # Saving the orderitem
                item.price = prices[index]
                item.quantity = quantities[index]
                item.stock = Stock.objects.get(id=stocklist[index])
                if types[index] != "None":
                    item.type = ProductType.objects.get(id=types[index])
                item.save()
            print(buyorder.get_total_cost())
            print(supplier)
            # supplier.credit += buyorder.get_total_cost()
            # supplier.save()
            return redirect('buyorder:buyorder_list')
    context = {
        'buyorderform': buyorderform,
        'buyorder': buyorder,
        'stocks': stocks,
    }
    return render(request, 'buyorder/buyorder_confirmation.html', context)


def buyorder_details(request, pk):
    order = BuyOrder.objects.get(id=pk)
    context = {
        'order': order
    }
    return render(request, 'buyorder/buyorder_details.html', context)


def buyorder_list(request):
    buyorders = BuyOrder.objects.all()
    context = {
        'buyorders': buyorders,

    }
    return render(request, 'buyorder/list_buyorder.html', context)


# pk from supplier view
# Billin Buy Order

def buyorderorder_list_by_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    buyorders = BuyOrder.objects.all().filter(supplier=supplier, factured=False)

    if request.method == 'POST':
        # get submitted orders
        chosenorders = request.POST.getlist("orders")
        # create billing object if there is selected orders
        if len(chosenorders) != 0:
            # print(chosenorders)
            # buyorderbill object
            buyorderbilling = BuyOrderBilling()
            buyorderbilling.supplier = supplier
            # TODO : Uncomment this line
            # buyorderbilling.user = request.user.id
            buyorderbilling.save()
            for orderid in chosenorders:
                # each order is a billing item
                currentorder = BuyOrder.objects.get(id=orderid)
                currentorder.factured = True
                currentorder.save()
                orderprice = currentorder.get_total_cost()
                # adding supplier credit
                supplier.credit += orderprice
                supplier.save()
                #                orderweight = currentorder.get_total_weight()
                BillBuyOrderItem.objects.create(
                    bill=buyorderbilling,
                    order=currentorder,
                    price=orderprice,
                    #                   weight=orderweight,
                )
                # increase quantity from the stock
                currentorderitems = currentorder.items.all()
                for item in currentorderitems:
                    stockitems = StockProduct.objects.all().filter(stock=item.stock)
                    itemexist = 1
                    # check if stock doesn't have the product
                    if len(stockitems) > 0:
                        # stock has products check if product exist
                        for stockitem in stockitems:
                            # the same product exist
                            if stockitem.product.id == item.product.id:
                                # Same Type
                                if stockitem.type == item.type:
                                    stockitem.quantity += int(item.quantity)
                                    stockitem.save()
                                    itemexist = 2
                                #                 # operation done same product plus the new quantity

                        if itemexist == 1:
                            #             # stock not empty product doesn't exist in it
                            #             # Or type doesn't exist
                            #             # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=int(item.quantity),
                                category=item.product.category,
                                stock=item.product.stock,
                                type=item.type
                            )
                    else:
                        #         # stock is empty
                        itemexist = 0
                        if itemexist == 0:
                            # create new stockproduct
                            StockProduct.objects.create(
                                product=item.product,
                                quantity=int(item.quantity),
                                category=item.product.category,
                                stock=item.product.stock,
                                type=item.type
                            )
            # send bill to be printed
            pk = buyorderbilling.pk
            return redirect(f'../../billingorder/buybill_pdf/{pk}')

    context = {
        'buyorders': buyorders
    }
    return render(request, 'buyorder/billing_list_buyorder.html', context)


def buyorder_pdf(request, pk):
    buyorder = get_object_or_404(BuyOrder, id=pk)
    html = render_to_string('buyorder/pdf.html', {'order': buyorder})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{buyorder.id}.pdf'

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def buyorder_delete(request, pk):
    order = get_object_or_404(BuyOrder, id=pk)
    if request.method == 'POST':
        if not order.factured:
            order.delete()
            return redirect('buyorder:buyorder_list')
        else:
            return redirect('buyorder:buyorder_list')
    context = {
        'order': order
    }
    return render(request, 'buyorder/buyorder_delete.html', context)
