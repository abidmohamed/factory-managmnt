import collections
import datetime
from django.contrib.auth.models import User, Group, Permission

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from accounts.decorators import admin_only, unauthneticated_user, allowed_user
from billingorder.models import OrderBilling
from caisse.models import Transaction
from customer.forms import UserForm
from customer.models import Customer
from order.models import Order
from payments.models import CustomerPayment, SupplierPayment
from product.models import Product, ProductType
from supplier.models import Supplier
from warehouse.models import StockProduct
from delivery.models import Delivery


@unauthneticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print('USER LOGED ------->', user)
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
@allowed_user(['admin', 'delivery', 'desk_helper'])
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

    # Caisse
    transactions = Transaction.objects.all()
    customerpayments = CustomerPayment.objects.all()
    supplierpayments = SupplierPayment.objects.all()

    # today Caisse
    today_transactions = Transaction.objects.all().filter(trans_date__year=now.year, trans_date__month=now.month,
                                                          trans_date__day=now.day)
    today_customerpayments = CustomerPayment.objects.all().filter(pay_date__year=now.year, pay_date__month=now.month,
                                                                  pay_date__day=now.day)
    today_supplierpayments = SupplierPayment.objects.all().filter(pay_date__year=now.year, pay_date__month=now.month,

                                                                  pay_date__day=now.day)
    today_caisse = 0
    caisse = 0
    ccp_caisse = 0
    cash_caisse = 0

    # Total Caisse Value
    for transaction in transactions:
        if transaction.Transaction_type == "Income":
            caisse += transaction.amount
            cash_caisse += transaction.amount
        else:
            caisse -= transaction.amount
            cash_caisse -= transaction.amount

    for customerpayment in customerpayments:
        if customerpayment.pay_status == "Cash":
            caisse += customerpayment.amount
            cash_caisse += customerpayment.amount
        else:
            ccp_caisse += customerpayment.amount

    for supplierpayment in supplierpayments:
        if supplierpayment.pay_status == "Cash":
            caisse -= supplierpayment.amount
            cash_caisse -= supplierpayment.amount
        else:
            ccp_caisse -= supplierpayment.amount

    # Today Caisse
    for transaction in today_transactions:
        if transaction.Transaction_type == "Income":
            today_caisse += transaction.amount
        else:
            today_caisse -= transaction.amount

    for customerpayment in today_customerpayments:
        # if customerpayment.pay_status == "Cash":
        today_caisse += customerpayment.amount

    for supplierpayment in today_supplierpayments:
        # if supplierpayment.pay_status == "Cash":
        today_caisse -= supplierpayment.amount

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
    productstype = ProductType.objects.all()
    stockproductsalertcount = 0
    for product in productstype:
        # print("TYPES ALERT ------>",StockProduct.objects.all().filter(type=product,
        # quantity__lte=product.alert_quantity))
        if StockProduct.objects.all().filter(type=product, quantity__lte=product.alert_quantity):
            stockproductsalertcount += 1

    group = request.user.groups.all()[0].name
    delivery_caisse = 0
    delivery = Delivery.objects.none()
    # to show caisse of delivery
    if group == 'delivery':
        print("#############> Delivery")
        delivery = Delivery.objects.get(user=request.user)
        delivery_caisse = delivery.money

    # check if we got a delivery
    if delivery is None:
        orderbills = OrderBilling.objects.none()
    else:
        orderbills = OrderBilling.objects.filter(delivery=delivery, paid=False)

    delivery_orders = Order.objects.none()
    order_caisse = 0
    for bill in orderbills:
        print("Bill ##########>", bill)
        for item in bill.items.all():
            print("item ############> ", item)
            # get orders
            delivery_orders |= Order.objects.filter(id=item.order.id)
            current_order = Order.objects.get(id=item.order.id)
            if not current_order.delivered:
                order_caisse += current_order.get_total_cost()

    context = {'customerscount': customerscount,
               'orderscount': orderscount, 'ordersnotdelivered': ordersnotdelivered, 'ordersdelivered': ordersdelivered,
               'supplierscount': supplierscount,
               'deliverymancount': deliverymancount, 'ordersfacturedcount': ordersfacturedcount,
               'monthlyorderscount': monthlyorderscount, 'monthlyordersdeliveredcount': monthlyordersdeliveredcount,
               'monthlyordersfacutredcount': monthlyordersfacutredcount, 'allOrders': allOrders,
               'stockproductsalertcount': stockproductsalertcount, 'cash_caisse': cash_caisse, 'ccp_caisse': ccp_caisse,
               'today_caisse': today_caisse, 'caisse': caisse, 'delivery_caisse': delivery_caisse,
               'orderbills': orderbills, 'delivery_orders': delivery_orders, 'order_caisse': order_caisse
               }
    return render(request, 'dashboard.html', context)


def add_user(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            if Group.objects.all().filter(name='desk_helper'):
                group = Group.objects.get(name='desk_helper')
            else:
                group = Group.objects.create(name='desk_helper')

            user.groups.add(group)

            user.save()
            # permission = Permission.objects.get(id=1)
            # print("Permissions ====>", Permission.objects.all())
            # user.user_permissions.add(5, 7)
            # print("User Permission ====>", user.user_permissions.all())
            # print(permission.name)

            return redirect('accounts:permissions_list', user.id)
        else:
            return redirect('')

    context = {
        'user_form': user_form,
    }
    return render(request, 'user/add_user.html', context)


def users_list(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "user/list_user.html", context)


def permissions_list(request, pk):
    user = User.objects.get(id=pk)
    permissions = Permission.objects.all()
    if request.method == 'POST':
        # print(request.POST.getlist('permission_chosen'))
        chosen_permissions = request.POST.getlist('permission_chosen')
        for permission in chosen_permissions:
            current_permission = Permission.objects.get(id=permission)
            print(current_permission)
            user.user_permissions.add(current_permission.id)
        user.save()
        return redirect("accounts:users_list")
    context = {
        'user': user,
        'permissions': permissions,
    }

    return render(request, 'user/permissions_list.html', context)
