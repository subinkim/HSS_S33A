from django.contrib import admin

# Register your models here.
from .models import Toppings, Category, Order, CustomerOrder

admin.site.register(Toppings)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(CustomerOrder)