import json

from django.utils.encoding import force_text
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from orders.models import Product, Order, ProductQuantity
from orders.serializers import OrderSerializer


class OrderException(APIException):
    """
    Custom APIException to return proper message in case of error.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = force_text(detail)


class OrderPrice(APIView):
    """
    Given an order returns the pricing information for that order.
    """

    @staticmethod
    def check_request_format(requested_data):
        """Checks the request to the api contains the requested information."""

        if ('order' not in requested_data or 'id' not in requested_data['order']
                or 'items' not in requested_data['order']):
            raise OrderException('Request does not contain the required '
                                 'information. Send an order id and some '
                                 'items in the order.',
                                 status.HTTP_400_BAD_REQUEST)

        for item in requested_data['order']['items']:
            if 'product_id' not in item or 'quantity' not in item:
                raise OrderException('Each item in the request needs to have '
                                     'a `product_id` and a `quantity`',
                                     status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def check_product_info(product_info):
        """
        Checks the product info has the correct format and it's present
        in the system
        """
        product_id = product_info['product_id']
        if not isinstance(product_id, int) or not isinstance(
                product_info['quantity'], int):
            raise OrderException('Product id and quantity of items need to '
                                 'be numbers',
                                 status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(product_id=product_info['product_id'])
        except Product.DoesNotExist:
            raise OrderException(f'Please check if the product id '
                                 f'{product_id} is in the system',
                                 status.HTTP_404_NOT_FOUND)
        return product

    def post(self, request):

        requested_data = json.loads(request.data['_content'])
        self.check_request_format(requested_data)

        requested_order = requested_data['order']
        order_id = requested_order['id']
        # TODO: validate currency code corresponds to the international standard
        currency = requested_order.get('currency')
        items = requested_order['items']

        try:
            # checks if we already have the order in the system
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = Order.objects.create(id=order_id, currency=currency)
            products_in_order = []
            for item in items:
                product = self.check_product_info(item)
                products_in_order.append(ProductQuantity.
                                         objects.create(order=order,
                                                        product=product,
                                                        quantity=item['quantity']))
            order.items.set(products_in_order)
            order.save()

        serialize_fields = ('id', 'items', 'currency', 'total_price',
                            'total_vat', 'customer')
        serializer = OrderSerializer(order,
                                     fields=serialize_fields)
        return Response(serializer.data)