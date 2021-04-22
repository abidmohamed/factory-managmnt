import decimal
from decimal import Decimal
from django.conf import settings
from product.models import Product
from product.models import ProductType


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart
        :param request:
        """
        # store current session
        self.session = request.session
        # get cart cart from session
        cart = self.session.get(settings.CART_SESSION_ID)
        # if no cart is present in the session
        if not cart:
            # save an empty cartin the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, product_type, quantity=1, override_quantity=False, price=0):
        """
                Add a product to the cart or update its quantity
                :param product_type:
                :param product:
                :param price:
                :param product: The product instance to add or update in the cart.
                :param quantity: An optional integer with the product quantity. This defaults to 1.
                :param override_quantity: This is a Boolean that indicates whether the quantity
                needs to be overridden with the given quantity (True), or whether the new
                quantity has to be added to the existing quantity (False).
                :return:
                """
        product_id = str(product.id)
        product_type_id = str(product_type.id)
        print("Cart.py --------")
        print(product_type_id)
        if product_type_id not in self.cart:
            self.cart[product_type_id] = {'quantity': 0,
                                          'price': str(price)
                                          }
        if override_quantity:
            self.cart[product_type_id]['quantity'] = int(quantity)
        else:
            self.cart[product_type_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product_type:
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate through the items contained in the cart and get the products
        from the database.
        :return:
        """
        product_ids = self.cart.keys()
        product_types_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = []
        for id_product in product_ids:
            products.append(id_product)
            print("Product ids-----------> ", id_product)
            # Product.objects.filter(id__in=product_ids)

        print("Products list length -------->", len(products))
        product_types = []
        for id_type in product_types_ids:
            product_types.append(id_type)
        # product_types = ProductType.objects.filter(product__in=product_types_ids)
        print("Products Types list length -------->", len(product_types))

        # copy the cart
        cart = self.cart.copy()
        for product_id, product_type_id in zip(products, product_types):
            product_type = ProductType.objects.get(id=product_type_id)
            cart[str(product_id)]['product'] = Product.objects.filter(id=product_type.product.id)
            cart[str(product_type_id)]['product_type'] = ProductType.objects.get(id=product_type_id)
            # print(product_type.product.id, "-------------------product")
            # print(product_type.id, "-------------------------type")
            # iterate through items in the cart
        for item in cart.values():
            # convert to decimal
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the Cart.
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        calculate the total cost of the items in the cart
        :return:
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
