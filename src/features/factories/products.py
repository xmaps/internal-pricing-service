import factory

from orders.models import Product, VatBand


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('product_id', 'price', 'vat_band')

    # Defaults (can be overwritten)
    product_id = 1
    price = '599'


class StandardVatBandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VatBand
        django_get_or_create = ('name', 'rate')

    # Defaults (can be overwritten)
    name = 'standard'
    rate = 0.2

    product_101 = factory.RelatedFactory(ProductFactory, 'vat_band',
                                       product_id=101, price=599)

    product_105 = factory.RelatedFactory(ProductFactory, 'vat_band',
                                       product_id=105, price=1250)


class ZeroVatBandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VatBand
        django_get_or_create = ('name', 'rate')

    # Defaults (can be overwritten)
    name = 'zero'
    rate = 0

    product_102 = factory.RelatedFactory(ProductFactory, 'vat_band',
                                       product_id=102, price=250)

    product_103 = factory.RelatedFactory(ProductFactory, 'vat_band',
                                       product_id=103, price=250)

    product_104 = factory.RelatedFactory(ProductFactory, 'vat_band',
                                       product_id=104, price=1000)



