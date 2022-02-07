from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User, Group

from billingorder.models import OrderBilling
from customer.forms import UserForm
from delivery.forms import DeliveryFrom
from delivery.models import Delivery
from accounts.decorators import admin_only
from order.models import Order


@admin_only
def add_delivery(request):
    user_form = UserForm()
    delivery_form = DeliveryFrom()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        delivery_form = DeliveryFrom(request.POST)

        if delivery_form.is_valid() and user_form.is_valid():

            user = user_form.save()
            delivery = delivery_form.save(commit=False)

            if Group.objects.all().filter(name='delivery'):
                group = get(name='delivery')
            else:
                group = Group.objects.create(name='delivery')

            user.groups.add(group)

            delivery.user = user

            delivery.save()

            print(request.POST)
            messages.success(request, "Created Successfully !")
            return redirect('delivery:delivery_list')
        else:
            messages.error(request, "ERROR HAPPENED !")
    context = {
        'user_form': user_form,
        'delivery_form': delivery_form
    }
    return render(request, 'delivery/add_delivery.html', context)


def delivery_list(request):
    deliveries = Delivery.objects.all()
    context = {
        'deliveries': deliveries
    }
    return render(request, 'delivery/list_delivery.html', context)


def update_delivery(request, pk):
    delivery = get_object_or_404(Delivery, id=pk)
    delivery_form = DeliveryFrom(instance=delivery)
    if request.method == 'POST':
        delivery_form = DeliveryFrom(request.POST, instance=delivery)
        if delivery_form.is_valid():
            delivery_form.save()
            return redirect('delivery:delivery_list')
    context = {
        'delivery_form': delivery_form
    }
    return render(request, 'delivery/add_delivery.html', context)


def delete_delivery(request, pk):
    delivery = get_object_or_404(Delivery, id=pk)
    context = {
        'delivery': delivery
    }
    if request.method == 'POST':
        delivery.delete()
        return redirect('delivery:delivery_list')
    return render(request, 'delivery/delete_delivery.html', context)


def details_delivery(request, pk):
    delivery = get_object_or_404(Delivery, id=pk)

    unpaidorderbills = OrderBilling.objects.filter(delivery=delivery, paid=False)
    paidorderbills = OrderBilling.objects.filter(delivery=delivery, paid=True)

    unpaid_order_caisse = 0

    delivery_orders = Order.objects.none()

    for bill in unpaidorderbills:
        print("Bill ##########>", bill)
        for item in bill.items.all():
            print("item ############> ", item)
            # get orders
            delivery_orders |= Order.objects.filter(id=item.order.id)
            current_order = Order.objects.get(id=item.order.id)
            if not current_order.delivered:
                unpaid_order_caisse += current_order.get_total_cost()

    context = {
        'delivery': delivery,
        'unpaid_order_caisse': unpaid_order_caisse
    }

    return render(request, 'delivery/details.html', context)
