from import_export import resources
from category.models import Category


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

        # fields = ["id", "category", "name", "ref", "desc", "stock"]
