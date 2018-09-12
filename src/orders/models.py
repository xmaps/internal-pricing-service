from django.db import models

from orders.utils import get_currency_rate


class VatBand(models.Model):
    """
    Represents the different vat classifications the products might have
    """
    name = models.CharField(unique=True, max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return f'VatBand: {self.name}'


class Product(models.Model):
    """
    Represents the different products present in the system
    """
    product_id = models.IntegerField(unique=True)
    price = models.PositiveIntegerField(default=0)
    vat_band = models.ForeignKey(VatBand, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(editable=False, default=False)

    @property
    def vat(self):
        if self.vat_band.rate == 0:
            return 0
        else:
            return round(self.price * self.vat_band.rate)

    class Meta:
        ordering = ["product_id"]
        verbose_name_plural = "Product"

    def __str__(self):
        return f'Product id: {self.product_id}'


class Order(models.Model):
    """
    Represents the order made to the system to process
    """
    id = models.IntegerField(primary_key=True)
    items = models.ManyToManyField(Product, through='ProductQuantity',
                                   blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(editable=False, default=False)

    def total_vat(self):
        total_vat = 0
        for item in self.items.all():
            quantity = item.productquantity_set.get(order=self.id).quantity
            total_item_vat = item.vat * quantity
            total_vat += total_item_vat

        if self.currency:
            rate = get_currency_rate("GBP", self.currency)
            total_vat = total_vat * rate

        return round(total_vat)

    def total_price(self):
        total_price = 0
        for item in self.items.all():
            quantity = item.productquantity_set.get(order=self.id).quantity
            total_item_vat = item.vat * quantity
            total_item_price = item.price * quantity
            total_price += total_item_price + total_item_vat

        if self.currency:
            rate = get_currency_rate("GBP", self.currency)
            total_price = total_price * rate

        return round(total_price)

    def __str__(self):
        return f'Order number: {self.id}'


class ProductQuantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return f"{self.order} - {self.product}, quantity: {self.quantity} "
