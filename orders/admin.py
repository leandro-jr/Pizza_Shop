from django.contrib import admin

from .models import Pizza, Toppings

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Toppings)
