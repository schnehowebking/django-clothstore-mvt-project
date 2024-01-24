from django.db import models
from accounts.models import *
from products.models import *


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.cartitem.all())
    def __str__(self) -> str:
        return f'{self.user.first_name}\'s Cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self) -> str:
        return f'{self.cart.user.first_name}\'s cart Items'