from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Review)    
admin.site.register(WishList)