import decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from billingorder.forms import BillingOrderForm
from billingorder.models import OrderBilling, BuyOrderBilling
from xhtml2pdf import pisa

from customer.models import Customer


def create_orderbill(request, pk):
    customers = Customer.objects.all()
    orderbill = OrderBilling.objects.get(id=pk)
    # print(str(orderbill))
    billingform = BillingOrderForm(instance=orderbill)
    if request.method == 'POST':
        billingform = BillingOrderForm(request.POST, instance=orderbill)
        if billingform.is_valid():
            chosencustomer = request.POST.getlist("customers")
            if len(chosencustomer) != 0:
                bill = billingform.save(commit=False)
                customer = Customer.objects.get(id=chosencustomer[0])

                bill.customer = customer
                bill.save()
                return redirect('billingorder:bill_list')
    context = {
        'billingform': billingform,
        'orderbill': orderbill,
        'customers': customers,
    }
    return render(request, "billingorder/add_bill.html", context)


def bill_list(request):
    bills = OrderBilling.objects.all()
    context = {'bills': bills}

    return render(request, 'billingorder/list_bill.html', context)


def delete_bill(request, pk):
    bill = get_object_or_404(OrderBilling, id=pk)
    context = {'bill': bill}
    if request.method == 'POST':
        bill.delete()

        return redirect('billingorder:bill_list')
    return render(request, 'billingorder/list_bill.html', context)


def bill_pdf(request, pk):
    bill = get_object_or_404(OrderBilling, id=pk)
    # total Cost and TVA and Timbre
    total_cost = bill.get_total_cost()
    # divided by 5
    total_cost = total_cost / 5
    # tva
    tva = round(total_cost * decimal.Decimal(0.19), 2)
    # TTC
    ttc = total_cost + tva
    html = render_to_string('billingorder/pdf.html', {'bill': bill, 'total_cost': total_cost, 'tva': tva, 'ttc': ttc})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=bill_{bill.id}.pdf'
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def buybill_list(request):
    bills = BuyOrderBilling.objects.all()
    context = {'bills': bills}

    return render(request, 'billingbuyorder/list_bill.html', context)


def delete_billbuy(request, pk):
    bill = get_object_or_404(BuyOrderBilling, id=pk)
    context = {'bill': bill}
    if request.method == 'POST':
        bill.delete()

        return redirect('billingorder:buybill_list')
    return render(request, 'billingbuyorder/list_bill.html', context)


def buybill_pdf(request, pk):
    bill = get_object_or_404(BuyOrderBilling, id=pk)
    html = render_to_string('billingbuyorder/pdf.html', {'bill': bill})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=bill_{bill.id}_{bill.supplier}.pdf'
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response