from django.contrib import admin
from .models import Order, OrderStatus, Product, ProductCategory, OrderProduct, Like, Favorite, Review

admin.site.register([ Order, OrderStatus, Product, ProductCategory, OrderProduct, Like, Favorite, Review])