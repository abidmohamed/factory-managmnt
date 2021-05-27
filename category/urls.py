from django.urls import path
from category import views

app_name = 'category'

urlpatterns = [

    path('all_category_list/', views.all_category_list, name='all_category_list'),
    path('category_list', views.category_list, name='category_list'),
    path('add_category', views.add_category, name='add_category'),
    path('update_category/<str:pk>', views.update_category, name='update_category'),
    path('delete_category/<str:pk>', views.delete_category, name='delete_category'),

    path('export_categories_excel', views.export_categories_excel, name='export_categories_excel'),
    path('upload_category_excel', views.upload_category_excel, name='upload_category_excel'),

]
