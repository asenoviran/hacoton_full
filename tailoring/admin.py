from django.contrib import admin
from .models import OrderTailoring, OrderStatus, Product, ProductCategory, OrderProduct, Like, Favorite, Review, Payment

admin.site.register([ OrderTailoring, OrderStatus, Product, ProductCategory, OrderProduct, Like, Favorite, Review, Payment])