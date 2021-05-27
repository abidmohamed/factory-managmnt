from import_export import resources

from product.models import Product, ProductType


class ProductsResource(resources.ModelResource):
    class Meta:
        model = Product

        # fields = ["id", "category", "name", "ref", "desc", "stock"]


class ProductTypeResource(resources.ModelResource):
    class Meta:
        model = ProductType
