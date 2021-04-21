from django.shortcuts import render, redirect

# Create your views here.
from buyorder.models import BuyOrder, BuyOrderItem
from category.models import Category
from order.models import Order, OrderItem
from product.forms import ProductForm, ProductTypeFormset, TypeFrom
from product.models import Product, ProductType


def add_product(request):
    if request.method == 'GET':
        productform = ProductForm()
    elif request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            product = productform.save()
            return redirect("product:add_product_type", product.id)
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)


def product_details(request, pk):
    product = Product.objects.get(id=pk)

    # types
    types = product.get_types()

    customers = []
    suppliers = []

    all_sell_order = Order.objects.all().filter(factured=True)
    all_buy_order = BuyOrder.objects.all().filter(factured=True)

    chosen_orders = []
    chosen_buyorders = []

    products_orders = OrderItem.objects.none()
    products_buyorders = BuyOrderItem.objects.none()

    sell_quantities = []
    buy_quantities = []

    sell_quantity = 0
    buy_quantity = 0

    # Sell orders product count
    for order in all_sell_order:
        # iterate items
        for item in order.items.all():
            # check if the item type is this product type
            for prod_type in types:
                if item.product_type.id == prod_type.id:
                    # 1- fill the chosen order the quantity of the product in this order
                    chosen_orders.append(order.id)
                    customers.append(order.customer)
                    # print(len(chosen_orders))
                    products_orders |= order.items.all().filter(product_type__id=item.product_type.id)
                    # print(len(products_orders))
                    sell_quantity += item.quantity
                    sell_quantities.append(item.quantity)
                    # print(len(sell_quantities))

    # Merge all the lists in one list
    final_list = zip(chosen_orders, customers, products_orders, sell_quantities)
    # for order, item, quantity in final_list:
    #     print(item, "Element")
    # Buy orders product count
    for order in all_buy_order:
        # iterate items
        for item in order.items.all():
            # check if the item is this product
            if item.product.id == product.id:
                # item found
                # iterate types
                for prod_type in types:
                    if item.type.id == prod_type.id:
                        # 1- fill the chosen order the quantity of the product in this order
                        chosen_buyorders.append(order.id)
                        suppliers.append(order.supplier)
                        products_buyorders |= order.items.all().filter(type__id=item.type.id)
                        buy_quantity += item.quantity
                        buy_quantities.append(item.quantity)
    # Merge all the lists in one list
    final_buylist = zip(chosen_buyorders, suppliers, products_buyorders, buy_quantities)
    context = {
        'product': product,
        'final_list': final_list,
        'final_buylist': final_buylist,
        'sell_quantity': sell_quantity,
        'buy_quantity': buy_quantity,
        'types': types,
    }
    return render(request, 'product/product_details.html', context)


# from add buyorder we can product
def add_product_buyorder(request, pk):
    # pk is city pk
    if request.method == 'GET':
        productform = ProductForm()
    elif request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        print("----------------BUY ORDER ADD PRODUCT")
        if productform.is_valid():
            product = productform.save()
            return redirect("product:add_product_type", product.id)
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)


def product_list(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.all().filter(category=category)
    context = {
        'products': products,
    }
    return render(request, 'product/list_product.html', context)


def all_product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product/all_product_list.html', context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    productform = ProductForm(instance=product)
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES, instance=product)
        if productform.is_valid():
            productform.save()
            return redirect('/')
    context = {'productform': productform}
    return render(request, 'product/add_product.html', context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'product/delete.html', context)


def add_type(request, pk):
    product = Product.objects.get(id=pk)
    productypeformset = ProductTypeFormset(queryset=ProductType.objects.none())
    if request.method == 'POST':
        productypeformset = ProductTypeFormset(request.POST)
        if productypeformset.is_valid():
            for typeform in productypeformset:
                producttype = typeform.save(commit=False)
                producttype.product = product
                producttype.save()

            return redirect('product:all_product_list')
    context = {
        'productypeformset': productypeformset,
    }
    return render(request, 'product/add_type.html', context)


def update_type(request, pk):
    prod_type = ProductType.objects.get(id=pk)
    typeform = TypeFrom(instance=prod_type)
    if request.method == 'POST':
        typeform = TypeFrom(request.POST, instance=prod_type)
        if typeform.is_valid():
            typeform.save()
            return redirect("product:all_product_list")

    context = {
        'typeform': typeform
    }
    return render(request, 'product/update_type.html', context)