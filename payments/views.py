from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
from customer.models import Customer
from payments.forms import CustomerPaymentForm, SupplierPaymentForm, CustomerChequeForm, SupplierChequeForm
from payments.models import SupplierPayment, CustomerPayment
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
