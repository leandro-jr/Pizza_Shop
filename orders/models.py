from django.db import models

class Pizza(models.Model):
    style = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.style} {self.flavor} for USD: {self.price}"

class Toppings(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"
