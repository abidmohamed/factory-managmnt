import collections
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from accounts.decorators import admin_only, unauthneticated_user
from customer.models import Customer
from family.forms import FamilyForm
from family.models import Family
from order.models import Order
from product.models import Product
from supplier.models import Supplier
from warehouse.models import StockProduct
from delivery.models import Delivery


@unauthneticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username Or Password Is not correct')
    context = {}
    return render(request, 'login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
@admin_only
def home(request):
    # now time
    now = datetime.datetime.now()
    customerscount = Customer.objects.all().count()
    orderscount = Order.objects.all().filter(created__year=now.year, factured=False).count()
    ordersnotdelivered = Order.objects.all().filter(created__year=now.year, delivered=False, factured=True).count()
    ordersdelivered = Order.objects.all().filter(created__year=now.year, delivered=True).count()
    supplierscount = Supplier.objects.all().count()
    deliverymancount = Delivery.objects.all().count()
    ordersfacturedcount = Order.objects.all().filter(factured=True).count()
    ordersfactured = Order.objects.all().filter(factured=True)

    # Monthly Orders
    monthlyorderscount = []
    monthlyordersfacutredcount = []
    monthlyordersdeliveredcount = []
    for i in range(1, 13):
        monthlyorderscount.append(Order.objects.all().filter(created__year=now.year, created__month=i).count())
        monthlyordersfacutredcount.append(Order.objects.all().filter(created__year=now.year, created__month=i,
                                                                     factured=True).count())
        monthlyordersdeliveredcount.append(Order.objects.all().filter(created__year=now.year, created__month=i,
                                                                      delivered=True).count())

    # Most Products bought
    allOrders = {}
    for order in ordersfactured:
        orderitems = order.items.all()
        for item in orderitems:
            if item.product.name in allOrders:
                allOrders[item.product.name] += item.quantity
            else:
                allOrders[item.product.name] = item.quantity

    # Sorting the values
    sorted_x = sorted(allOrders.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dict = collections.OrderedDict(sorted_x)
    print(sorted_dict)
    print({k: v for k, v in sorted(allOrders.items(), key=lambda item: item[1])})
    products = Product.objects.all()
    stockproductsalertcount = 0
    for product in products:
        pass
        # stockproductsalertcount = StockProduct.objects.all().filter(quantity__lte=product.alert_quantity).count()

    context = {'customerscount': customerscount,
               'orderscount': orderscount, 'ordersnotdelivered': ordersnotdelivered, 'ordersdelivered': ordersdelivered,
               'supplierscount': supplierscount,
               'deliverymancount': deliverymancount, 'ordersfacturedcount': ordersfacturedcount,
               'monthlyorderscount': monthlyorderscount, 'monthlyordersdeliveredcount': monthlyordersdeliveredcount,
               'monthlyordersfacutredcount': monthlyordersfacutredcount, 'allOrders': allOrders,
               'stockproductsalertcount': stockproductsalertcount,
               }
    return render(request, 'dashboard.html', context)
