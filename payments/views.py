from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from customer.models import Customer
from delivery.models import Delivery
from order.models import Order
from order.serializers import SellOrderSerializer
from payments.forms import CustomerPaymentForm, SupplierPaymentForm, CustomerChequeForm, SupplierChequeForm, \
    SellerPaymentForm
from payments.models import SupplierPayment, CustomerPayment, SellerPayment
from payments.serializers import CustomerPaymentSerializer
from seller.models import Seller, NoStockSeller
from supplier.models import Supplier


def customer_pay(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        payform = CustomerPaymentForm()
    elif request.method == 'POST':
        payform = CustomerPaymentForm(request.POST)
        if payform.is_valid():
            payment = payform.save(commit=False)
            payment.user = request.user.id
            payment.customer = customer
            customer.debt = customer.debt - payment.amount
            payment.save()
            customer.save()

            if payment.pay_status == "Cheque":
                return redirect(f'../create_customer_cheque/{payment.pk}')
            return redirect('customer:customer_list')

    context = {
        'payform': payform,
    }
    return render(request, 'payments/payment.html', context)


def delivery_customer_pay(request, pk):
    order = get_object_or_404(Order, id=pk)
    customer = Customer.objects.get(id=order.customer.pk)
    if request.method == 'GET':
        payform = CustomerPaymentForm()
    elif request.method == 'POST':
        payform = CustomerPaymentForm(request.POST)
        if payform.is_valid():
            payment = payform.save(commit=False)
            payment.user = request.user.id
            payment.customer = customer
            customer.debt = customer.debt - payment.amount
            # Get delivery guy
            delivery = get_object_or_404(Delivery, user=request.user)
            delivery.money += order.get_total_cost()

            delivery.save()
            payment.save()
            customer.save()

            # check if order paid
            if order.get_total_cost() == payment.amount:
                order.paid = True

            if payment.pay_status == "Cheque":
                return redirect(f'../create_customer_cheque/{payment.pk}')
            return redirect('accounts:home')

    context = {
        'payform': payform,
    }
    return render(request, 'payments/payment.html', context)




def create_customer_cheque(request, pk):
    customerpayment = CustomerPayment.objects.get(id=pk)
    chequeform = CustomerChequeForm()
    if request.method == "POST":
        chequeform = CustomerChequeForm(request.POST)
        if chequeform.is_valid():
            customercheque = chequeform.save(commit=False)
            customercheque.customer = customerpayment.customer
            customercheque.customerpayment = customerpayment
            customercheque.save()
            return redirect("payments:customer_paylist")

    context = {
        "chequeform": chequeform
    }
    return render(request, 'payments/create_cheque.html', context)


def customer_paylist(request):
    customerspayments = CustomerPayment.objects.all()
    context = {
        'customerspayments': customerspayments,
    }
    return render(request, 'payments/customer_pay_list.html', context)


def supplier_pay(request, pk):
    supplier = Supplier.objects.get(id=pk)
    if request.method == 'GET':
        payform = SupplierPaymentForm()
    elif request.method == 'POST':
        payform = SupplierPaymentForm(request.POST)
        if payform.is_valid():
            payment = payform.save(commit=False)
            payment.user = request.user.id
            payment.supplier = supplier
            supplier.credit = supplier.credit - payment.amount
            payment.save()
            supplier.save()
            if payment.pay_status == "Cheque":
                return redirect(f'../create_supplier_cheque/{payment.pk}')
            return redirect('supplier:supplier_list')

    context = {
        'payform': payform,
    }
    return render(request, 'payments/payment.html', context)


def create_supplier_cheque(request, pk):
    supplierpayment = SupplierPayment.objects.get(id=pk)
    chequeform = SupplierChequeForm()
    if request.method == "POST":
        chequeform = SupplierChequeForm(request.POST)
        if chequeform.is_valid():
            suppliercheque = chequeform.save(commit=False)
            suppliercheque.supplier = supplierpayment.supplier
            suppliercheque.supplierpayment = supplierpayment
            suppliercheque.save()
            return redirect("supplier:supplier_list")

    context = {
        "chequeform": chequeform
    }
    return render(request, 'payments/create_cheque.html', context)


def supplier_paylist(request):
    supplierspayments = SupplierPayment.objects.all()
    context = {
        'supplierspayments': supplierspayments,
    }
    return render(request, 'payments/supplier_pay_list.html', context)


def seller_pay(request, pk):
    seller = get_object_or_404(Seller, id=pk)
    payform = SellerPaymentForm()
    if request.method == 'GET':
        payform = SellerPaymentForm()
    elif request.method == 'POST':
        payform = SellerPaymentForm(request.POST)
        if payform.is_valid():
            payment = payform.save(commit=False)
            payment.user = request.user.id
            payment.seller = seller
            seller.debt = seller.debt - payment.amount
            payment.save()
            seller.save()

            return redirect('seller:list_seller')

    context = {
        'payform': payform,
    }
    return render(request, 'payments/payment.html', context)


def seller_paylist(request):
    sellerspayments = SellerPayment.objects.all()
    context = {
        'sellerspayments': sellerspayments,
    }
    return render(request, 'payments/seller_pay_list.html', context)


class ApiDeliveryCustomerPay(CreateAPIView):
    serializer_class = CustomerPaymentSerializer

    def perform_create(self, serializer):
        customer = get_object_or_404(Customer, id=self.request.data.get('customer'))
        delivery = get_object_or_404(Delivery, user=self.request.user)

        user = self.request.user
        user_seller = user.no_stock_seller
        logged_seller = get_object_or_404(NoStockSeller, id=user_seller.id)

        delivery.money += self.request.data.get('amount')
        delivery.save()

        customer.debt = customer.debt - self.request.data.get('amount')
        customer.save()

        return serializer.save(customer=customer, user=self.request.user.id)


class ApiSellerCustomerPay(CreateAPIView):
    serializer_class = CustomerPaymentSerializer

    def perform_create(self, serializer):
        customer = get_object_or_404(Customer, id=self.request.data.get('customer'))
        # delivery = get_object_or_404(Delivery, user=self.request.user)

        user = self.request.user
        user_seller = user.no_stock_seller
        logged_seller = get_object_or_404(NoStockSeller, id=user_seller.id)

        logged_seller.money += self.request.data.get('amount')
        logged_seller.save()

        customer.debt = customer.debt - self.request.data.get('amount')
        customer.save()

        return serializer.save(seller=logged_seller, customer=customer, user=self.request.user.id)


def list_customer_pay(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    payments = CustomerPayment.objects.filter(customer=customer)
    serializer = CustomerPaymentSerializer(payments, many=True)
    return Response(serializer.data)
