from django.contrib import admin
from .models import Order, OrderStatus, Document, Employee, Product, ProductCategory, OrderProduct

admin.site.register([ Order, OrderStatus, Document, Employee, Product, ProductCategory, OrderProduct])