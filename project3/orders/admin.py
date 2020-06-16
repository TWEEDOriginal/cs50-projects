from django.contrib import admin
from .models import *

# Register your models here.

class CartItemInline(admin.StackedInline):
      model = CartItem.toppings.through
      extra = 1

class ToppingAdmin(admin.ModelAdmin):
       inlines = [CartItemInline]    

class CartItemAdmin(admin.ModelAdmin):     
      filter_horizontal = ("toppings",)                  

admin.site.register(Regular_pizza)      
admin.site.register(Sicilian_pizza)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(CartItem, CartItemAdmin)      
admin.site.register(OrderItem)

