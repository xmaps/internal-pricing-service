from behave import when, then
from django.core.management import call_command

from orders.models import VatBand, Product


@when(u'I import the data from file {file_path}')
def import_pricing_data_from_file(context, file_path):
    call_command('import_data', file_path)


@then(u'I should have a VatBand object with name {vat_name}')
def should_have_vat_band_object(context, vat_name):
    assert VatBand.objects.get(name=vat_name) is not None


@then(u'I should have Product objects with {product_id} and {price}')
def should_have_product_object(context, product_id, price):
    # there should only one product with that id
    assert Product.objects.filter(product_id=product_id).count() == 1

    # get just the first one
    product = Product.objects.get(product_id=product_id)

    assert product.product_id is not None
    assert product.price is not None
    assert product.vat_band is not None
    assert product.created_at is not None
