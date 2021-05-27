from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from tablib import Dataset

from category.forms import CategoryForm
from category.models import Category
from category.resources import CategoryResource
from customer.models import Customer


def add_category(request):
    if request.method == 'GET':
        categoryform = CategoryForm()
    elif request.method == 'POST':
        categoryform = CategoryForm(request.POST, request.FILES)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('/')
    context = {'categoryform': categoryform}
    return render(request, 'category/add_category.html', context)


def category_list(request):
    categories = Category.objects.all()
    customer = Customer.objects.get(user=request.user)

    context = {
        'categories': categories,
        'customer': customer,
    }
    return render(request, 'category/list_category.html', context)


def all_category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category/all_list_category.html', context)


def update_category(request, pk):
    category = Category.objects.get(id=pk)
    categoryform = CategoryForm(instance=category)
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST, request.FILES, instance=category)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('/')
    context = {'categoryform': categoryform}
    return render(request, 'category/add_category.html', context)


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    context = {'category': category}
    if request.method == 'POST':
        category.delete()

        return redirect('/')
    return render(request, 'category/delete_category.html', context)


# Excel
def export_categories_excel(request):
    category_resource = CategoryResource()
    dataset = category_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="category.xls"'

    return response


def upload_category_excel(request):
    if request.method == 'POST':
        category_resource = CategoryResource()
        dataset = Dataset()
        new_category = request.FILES['myfile']

        if not new_category.name.endswith('xls'):
            messages.info(request, "Wrong Format")
            return render(request, 'category/upload.html')

        imported_data = dataset.load(new_category.read(), format='xls')
        for data in imported_data:
            value = Category(
                data[0], data[1],
            )
            value.save()
    return render(request, "category/upload.html")
