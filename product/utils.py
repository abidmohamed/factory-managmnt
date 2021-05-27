import xlwt
from django.http import HttpResponse


def export_products_xls(request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws_category = wb.add_sheet('Categories')
    ws = wb.add_sheet('Products')
    ws_type = wb.add_sheet('Types')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # extracting our model
    # model = queryset.model
    # model_fields = model._meta.fields + model._meta.many_to_many

    # adding fields name to columns
    columns_category = ["id", "Name"]
    columns = ["id", "Category_id", "Nom", "Code", "Description", "Stock"]
    columns_type = ["id", "Produit_id", "Name","Prix 1", "Prix 2", "Prix 3", "Prix 4", "Prix 5", "Prix 6",
                    "Prix Achat", "Quantity Alert", "Quantity Box", "Poids"]

    # Category
    for col_num in range(len(columns_category)):
        ws_category.write(row_num, col_num, columns_category[col_num], font_style)

    # Product
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Type
    for col_num in range(len(columns_type)):
        ws_type.write(row_num, col_num, columns_type[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
