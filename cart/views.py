from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from customer.models import Customer
from product.models import Product, ProductType
from warehouse.models import StockProduct
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    # print(request.POST)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        print(request.POST)
    customer = Customer.objects.get(user=request.user)
    customertype = customer.customer_type

    # get all quantities from product types
    cartform = CartAddProductForm(request.POST)
    quantities = request.POST.getlist('quantity')
    overrides = request.POST.getlist('override')
    types = request.POST.getlist('types')
    # counter to check that all elements validated
    validate = 0
    # iterate through elements and validate each from and add to cart
    for index, quantity in enumerate(quantities):
        # if the quantity selected by user isn't 0
        print(quantity)
        if quantity != "0":
            cartform.quantity = quantities[index]
            cartform.override = overrides[index]
            print(types[index])
            product_type = ProductType.objects.get(name=types[index])
            print(product_type.id)
            if cartform.is_valid():
                validate += 1
                print("This is valid !!!")
                cd = cartform.cleaned_data
                print(cd)
                print(product)
                if customertype == 'type1':
                    price = product_type.price1
                elif customertype == 'type2':
                    price = product_type.price2
                elif customertype == 'type3':
                    price = product_type.price3
                elif customertype == 'type4':
                    price = product_type.price4
                elif customertype == 'type5':
                    price = product_type.price5
                elif customertype == 'type6':
                    price = product_type.price6
                else:
                    price = 0.0

                cart.add(product=product,
                         product_type=product_type,
                         quantity=cartform.quantity,
                         override_quantity=cd['override'],
                         price=price
                         )
        else:
            validate += 1
    if len(quantities) == validate:
        return redirect('cart:cart_detail')


@require_POST
def update_cart(request, product_type_id):
    # print(request.POST)
    cart = Cart(request)
    # get type
    product_type = get_object_or_404(ProductType, id=product_type_id)
    # get type product
    product = get_object_or_404(Product, id=product_type.product.id)

    # get customer & customer type
    customer = Customer.objects.get(user=request.user)
    customertype = customer.customer_type

    # get all quantities from product types
    cartform = CartAddProductForm(request.POST)
    quantities = request.POST.getlist('quantity')
    overrides = request.POST.getlist('override')
    # counter to check that all elements validated
    validate = 0
    # iterate through elements and validate each from and add to cart
    for index, quantity in enumerate(quantities):
        # if the quantity selected by user isn't 0
        print(quantity)
        if quantity != "0":
            cartform.quantity = quantities[index]
            cartform.override = overrides[index]
            print(product_type.id)
            if cartform.is_valid():
                validate += 1
                print("This is valid !!!")
                cd = cartform.cleaned_data
                print(cd)
                print(product)
                if customertype == 'type1':
                    price = product_type.price1
                elif customertype == 'type2':
                    price = product_type.price2
                elif customertype == 'type3':
                    price = product_type.price3
                elif customertype == 'type4':
                    price = product_type.price4
                elif customertype == 'type5':
                    price = product_type.price5
                elif customertype == 'type6':
                    price = product_type.price6
                else:
                    price = 0.0

                cart.add(product=product,
                         product_type=product_type,
                         quantity=cartform.quantity,
                         override_quantity=cd['override'],
                         price=price
                         )
        else:
            validate += 1
    if len(quantities) == validate:
        return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    product_type = get_object_or_404(ProductType, id=product_id)
    cart.remove(product_type)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    customer = Customer.objects.get(user=request.user)
    print("-------------------------------------Cart Detail -------------------------------")
    for item in cart:
        print(item)
        # create an instance of CartAddProductForm for each item in the cart to allow
        # changing product quantities.
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'customer': customer})
