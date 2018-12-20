from django.contrib import admin

from .models import Pizza, Toppings, Shopping_Cart, Placed_Orders, Pasta, Salads, Dinner, Subs, AddOn

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Toppings)
admin.site.register(Subs)
admin.site.register(AddOn)
admin.site.register(Pasta)
admin.site.register(Salads)
admin.site.register(Dinner)
admin.site.register(Shopping_Cart)
admin.site.register(Placed_Orders)
