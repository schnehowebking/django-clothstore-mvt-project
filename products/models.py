from django.db import models
from django.urls import reverse
from categories.models import *
from django.contrib.auth.models import User
from django.db.models import Count, Avg, ExpressionWrapper, F, fields




class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/media/", blank=True, null=True)

    def get_avg_rating(self):
        return self.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def get_popularity(self):
        return (self.purchase_set.count() + self.get_avg_rating()) / 2

    def __str__(self):
        return self.name
    
STAR_CHOICES = [
    ('1', '⭐'),
    ('2', '⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('5', '⭐⭐⭐⭐⭐'),
]

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name = "reviews",  on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
    def __str__(self):
        return f"Customer : {self.reviewer.first_name} - Product {self.product.name}"
    
class WishList(models.Model):
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.first_name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product}-{self.purchase_date}"