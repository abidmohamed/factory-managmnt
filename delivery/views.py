from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User, Group
from customer.forms import UserForm
from delivery.forms import DeliveryFrom
from delivery.models import Delivery
from accounts.decorators import admin_only


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
                group = Group.objects.get(name='delivery')
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
    delivery = Delivery.objects.get(id=pk)
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
    delivery = Delivery.objects.get(id=pk)
    context = {
        'delivery': delivery
    }
    if request.method == 'POST':
        delivery.delete()
        return redirect('delivery:delivery_list')
    return render(request, 'delivery/delete_delivery.html', context)
