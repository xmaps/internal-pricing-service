import json

from django.core.management.base import BaseCommand, CommandError

from orders.models import VatBand, Product


class PricingException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class PricingFormatter(object):
    """
    Processes, validates and formats the information from the pricing file.
    """
    @classmethod
    def process_product_data(cls, pricing_info):
        """
        Processes product data for the system.
        :param pricing_info: Products for the system json format
        :return: products data and vat bands
        """
        if 'prices' not in pricing_info or 'vat_bands' not in pricing_info:
            raise PricingException('Json data does not contain required '
                                   'product and vat band information')

        product_prices = pricing_info['prices']
        vat_bands = pricing_info['vat_bands']

        processed_vat_bands = {}
        for vat_name, vat_rate in vat_bands.items():
            if vat_name in processed_vat_bands:
                raise PricingException('Vat names need to be unique. '
                                       f'Vat names duplicated {vat_name}')

            try:
                rate = float(vat_rate)
            except ValueError:
                raise PricingException('Vat rates need to be a decimal. '
                                       f'Vat rate: {vat_rate}')

            processed_vat_bands[vat_name] = {
                'name': vat_name,
                'rate': rate
            }

        processed_products = {}
        for product_price in product_prices:
            product_id = product_price['product_id']
            if product_id in processed_products:
                raise PricingException('Product ids need to be unique. '
                                       f'Product id duplicated {product_id}')

            associated_vat_band = product_price['vat_band']
            if associated_vat_band not in processed_vat_bands:
                raise PricingException('Vat band does not exist. '
                                       f'Vat band: {associated_vat_band} on '
                                       f'product id: {product_id}')

            try:
                price = int(product_price['price'])
            except ValueError:
                raise PricingException('Product prices need to be numbers. '
                                       f'Price: {price} on '
                                       f'product id: {product_id}')

            processed_products[product_id] = {
                'product_id': product_id,
                'price': price,
                'vat_band': associated_vat_band
            }

        return processed_vat_bands, processed_products


class Command(BaseCommand):
    help = ('Imports product data from file (product and vatband). '
            'Argument is file path to json formatted file(s) representing a '
            'city forecast')

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['file_path']:
            with open(file_path, 'r') as pricing_file:
                json_data = json.load(pricing_file)
                try:
                    vat_bands, products = PricingFormatter.process_product_data(json_data)
                except PricingException as import_error:
                    raise CommandError(import_error.message)

                # Update of create vat bands
                for vat in vat_bands.values():
                    try:
                        obj = VatBand.objects.get(name=vat.get('name'))
                        obj.rate = vat.get('rate')
                        obj.save()
                    except VatBand.DoesNotExist:
                        obj = VatBand(**vat)
                        obj.save()
                    finally:
                        vat_bands[vat.get('name')].update({'obj': obj})

                # Update of create products
                for product in products.values():
                    associated_vat = product.pop('vat_band')
                    try:
                        obj = Product.objects.get(product_id=product.get('product_id'))
                        for key, value in product.items():
                            setattr(obj, key, value)
                        obj.vat_band = vat_bands[associated_vat]['obj']
                        obj.save()
                    except Product.DoesNotExist:
                        obj = Product(vat_band=vat_bands[associated_vat]['obj'],
                                      **product)
                        obj.save()

                self.stdout.write(self.style.SUCCESS('Successfully imported '
                                                     'data of "%s"' % file_path)
                                  )
