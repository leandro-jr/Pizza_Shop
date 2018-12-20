from django.db import models

#pizza
class Pizza(models.Model):
    style = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.style} {self.flavor} for USD: {self.price}"

#toppings to be added to teh pizzas
class Toppings(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"

#subs
class Subs(models.Model):
    size = models.CharField(max_length=64)
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.flavor} {self.size} for USD: {self.price}"

#add ons to be added to the subs
class AddOn(models.Model):
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.flavor} for USD: {self.price}"

#pasta
class Pasta(models.Model):
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.flavor} for USD: {self.price}"

#salads
class Salads(models.Model):
    flavor = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.flavor} for USD: {self.price}"

#dinner platters
class Dinner(models.Model):
    flavor = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.flavor} {self.size} for USD: {self.price}"

#shopping cart
class Shopping_Cart(models.Model):
    user = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    order_pizza = models.ManyToManyField(Pizza, blank=True, related_name="orders_pizza")
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="toppings")
    order_subs = models.ManyToManyField(Subs, blank=True, related_name="orders_subs")
    addons = models.ManyToManyField(AddOn, blank=True, related_name="addons")
    order_pasta = models.ManyToManyField(Pasta, blank=True, related_name="orders_pasta")
    order_salads = models.ManyToManyField(Salads, blank=True, related_name="orders_salads")
    order_dinner = models.ManyToManyField(Dinner, blank=True, related_name="orders_dinner")
    confirmed = models.BooleanField()

    def __str__(self):
        return f"{self.user}, {self.type}"

#same as shopping cart but only when purchase is confirmed
class Placed_Orders(models.Model):
    placed_order = models.ForeignKey(Shopping_Cart, on_delete=models.CASCADE, related_name="placed_orders")

    def __str__(self):
        return f"{self.placed_order}"
