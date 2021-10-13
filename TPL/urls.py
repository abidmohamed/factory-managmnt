"""TPL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from TPL import settings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('accounts.urls', namespace='accounts')),
    path('category/', include('category.urls', namespace='category')),
    path('product/', include('product.urls', namespace='product')),
    path('warehouse/', include('warehouse.urls', namespace='warehouse')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('delivery/', include('delivery.urls', namespace='delivery')),
    path('supplier/', include('supplier.urls', namespace='supplier')),
    path('order/', include('order.urls', namespace='order')),
    path('buyorder/', include('buyorder.urls', namespace='buyorder')),
    path('billingorder/', include('billingorder.urls', namespace='billingorder')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('caisse/', include('caisse.urls', namespace='caisse')),
    path('seller/', include('seller.urls', namespace='seller')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
