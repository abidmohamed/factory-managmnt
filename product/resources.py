from import_export import resources, widgets, fields

from category.models import Category
from product.models import Product, ProductType
from warehouse.models import Stock


class CharRequiredWidget(widgets.CharWidget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            return val
        else:
            raise ValueError('this field is required')


class ForeignkeyRequiredWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            print(self.field, value)
            return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value})
        else:
            raise ValueError(self.field + " required")


class ProductsResource(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category',
                            widget=ForeignkeyRequiredWidget(Category, 'name')
                            )
    stock = fields.Field(column_name='stock', attribute='stock',
                         widget=ForeignkeyRequiredWidget(Stock, 'name')
                         )

    class Meta:
        model = Product
        fields = ("id", "category", "name", "ref", "desc", "stock")
        clean_model_instances = True


class ProductTypeResource(resources.ModelResource):
    product = fields.Field(column_name='product', attribute='product',
                           widget=ForeignkeyRequiredWidget(Product, 'name')
                           )

    class Meta:
        model = ProductType

        fields = ('id', 'product', 'name', 'price1', 'price2', 'price3', 'price4', 'price5', 'price6'
                  , 'buyprice', 'alert_quantity', 'box_quantity', 'weight')
        clean_model_instances = True

# class CommentResource(resources.ModelResource):
#     category = fields.Field(column_name='category', attribute='category',
#                             widget=ForeignkeyRequiredWidget(Category, 'title'),
#                             saves_null_values=False)  # title Category modelindeki kolon ismi
#     description = fields.Field(saves_null_values=False, column_name='description', attribute='description',
#                                widget=CharRequiredWidget())
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'description', 'category')
#         clean_model_instances = True
