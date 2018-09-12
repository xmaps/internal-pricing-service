import math

from rest_framework import serializers
from orders.models import Product, Order, ProductQuantity


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProductQuantitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="product.id")
    vat = serializers.ReadOnlyField(source="product.vat_band.rate")
    price = serializers.ReadOnlyField(source="product.price")

    class Meta:
        model = ProductQuantity
        fields = ('id', 'quantity', 'price', 'vat')


class OrderSerializer(DynamicFieldsModelSerializer):
    items = ProductQuantitySerializer(source="productquantity_set", many=True,
                                      read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'items', 'currency')

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['total_price'] = instance.total_price()
        ret['total_vat'] = instance.total_vat()
        ret['customer'] = {}

        if instance.currency is None:
            del ret['currency']

        return ret
