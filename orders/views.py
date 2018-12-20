from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import stripe
import os

from django.core.mail import EmailMessage

from .models import Pizza, Toppings, Shopping_Cart, Placed_Orders, Pasta, Salads, Dinner, Subs, AddOn


def index(request):
    """render login if user is not registered or render menu otherwise"""
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})

    sici_small = Pizza.objects.filter(style="Sicilian", size="small")
    sici_large = Pizza.objects.filter(style="Sicilian", size="large")
    regular_small = Pizza.objects.filter(style="regular", size="small")
    regular_large = Pizza.objects.filter(style="regular", size="large")
    sub_steak_addons = AddOn.objects.exclude(flavor="Extra Cheese on any sub").all()
    sub_addons = AddOn.objects.filter(flavor="Extra Cheese on any sub").all()
    context = {
        "user": request.user,
        "pizzas": Pizza.objects.all(),
        "subs": Subs.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salads.objects.all(),
        "dinners": Dinner.objects.all(),
        "toppings": Toppings.objects.all(),
        "addons": AddOn.objects.all(),
        "sici_smalls": sici_small,
        "sici_larges": sici_large,
        "regular_smalls": regular_small,
        "regular_larges": regular_large,
        "sub_steak_addons": sub_steak_addons,
        "sub_addons": sub_addons
    }
    return render(request, "users/user.html", context)

def login_view(request):
    """login"""
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    """logout"""
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def register_view(request):
    """register user"""
    username = request.POST["username"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    if password == confirm_password:
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name )
        return render(request, "users/login.html", {"message": "Registered"})
    else:
        return render(request, "users/login.html", {"message": "Passwords do not match."})

def order_pizza(request):
    """use pizza.id as primary key and add it to the shopping cart. Render topping as output"""
    pizza_id = int(request.POST["pizza"])
    pizza = Pizza.objects.get(pk=pizza_id)
    user = request.user

    sc = Shopping_Cart(user=user, type="pizza", confirmed=False)
    sc.save()
    sc.order_pizza.add(pizza)

    message = ""
    topping_number = ""

    flavor = pizza.flavor
    if flavor == 'Cheese':
        message = 'No toppings will be added'
    elif flavor == 'Special':
        message = 'Margueritta  pizza with mozzarella di bufala, italian tomato and basil'
    else:
        topping_number = int(flavor[0])

    context = {
        "pizza": pizza,
        "user": request.user,
        "topping_number": topping_number,
        "toppings": Toppings.objects.all(),
        "message": message
    }
    return render(request, "users/topping.html", context)

def order_toppings(request):
    """use topping.id to add topping to shopping cart"""
    if request.method == "POST":
        topping_id = request.POST.getlist("topping")

        #last order
        sc = Shopping_Cart.objects.last()
        flavor = sc.order_pizza.first().flavor

        # check if number of toppings match the order
        topping_number = int(flavor[0])
        if topping_number != len(topping_id):
            sc.delete()
            return render(request, "users/topping.html", {"error": "You must choose the correct number of toppings"})

        for t in topping_id:
            topping = Toppings.objects.get(pk=t)
            sc.toppings.add(topping)

    return HttpResponseRedirect(reverse("shopping_cart"))

def order_subs(request):
    """use subs.id to add subs to shopping cart. Render topping as output"""
    sub_id = int(request.POST["sub"])
    sub = Subs.objects.get(pk=sub_id)
    user = request.user

    sc = Shopping_Cart(user=user, type="subs", confirmed=False)
    sc.save()
    sc.order_subs.add(sub)

    context = {
        "sub": sub,
        "user": request.user,
        "addons": AddOn.objects.all()
    }
    return render(request, "users/addon.html", context)

def order_addon(request):
    """use addons.id to add addons to shopping cart. Render topping as output"""
    if request.method == "POST":
        addon_id = request.POST.getlist("addon")

        sc = Shopping_Cart.objects.last()
        sub = sc.order_subs

        flavor = sc.order_subs.first().flavor

        #extras to steak + chees
        if flavor == "Steak + Cheese":
            for a in addon_id:
                addon = AddOn.objects.get(pk=a)
                sc.addons.add(addon)

        # extras to other subs
        else:
            if len(addon_id) != 1:
                context = {
                    "sub": sub,
                    "user": request.user,
                    "addons": AddOn.objects.all(),
                    "error": "You can only add Extra Cheese for this sub"
                }
                return render(request, "users/addon.html", context)

            else:
                if int(addon_id[0]) == AddOn.objects.get(flavor="Extra Cheese on any sub").id:
                    addon = AddOn.objects.get(pk=addon_id[0])
                    sc.addons.add(addon)
                else:
                    context = {
                        "sub": sub,
                        "user": request.user,
                        "addons": AddOn.objects.all(),
                        "error": "You can only add Extra Cheese for this sub"
                    }
                    return render(request, "users/addon.html", context)


    return HttpResponseRedirect(reverse("shopping_cart"))

def order_pasta(request):
    """use pasta.id to add pasta to shopping cart"""
    pasta_id = int(request.POST["pasta"])
    pasta = Pasta.objects.get(pk=pasta_id)
    user = request.user

    sc = Shopping_Cart(user=user, type="pasta", confirmed=False)
    sc.save()
    sc.order_pasta.add(pasta)

    return HttpResponseRedirect(reverse("shopping_cart"))

def order_salads(request):
    """use salads.id to add salads to shopping cart"""
    salads_id = int(request.POST["salads"])
    salads = Salads.objects.get(pk=salads_id)
    user = request.user

    sc = Shopping_Cart(user=user, type="salads", confirmed=False)
    sc.save()
    sc.order_salads.add(salads)

    return HttpResponseRedirect(reverse("shopping_cart"))

def order_dinner(request):
    """use dinner.id to add dinner platter to shopping cart"""
    dinner_id = int(request.POST["dinner"])
    dinner = Dinner.objects.get(pk=dinner_id)
    user = request.user

    sc = Shopping_Cart(user=user, type="dinner", confirmed=False)
    sc.save()
    sc.order_dinner.add(dinner)

    return HttpResponseRedirect(reverse("shopping_cart"))

def shopping_cart(request):
    """create list with all items of a user's shopping cart. For pizzas and subs there is a nested list with toppings/addons"""
    user = request.user
    orders = Shopping_Cart.objects.filter(user=user)
    orders_list_pizza = []
    orders_list_subs = []
    orders_list_pasta = []
    orders_list_salads = []
    orders_list_dinner = []
    total = 0

    for order in orders:
        if not order.confirmed:
            inside_list = []

            if order.type == "pizza":

                total += order.order_pizza.first().price

                inside_list.append(order.order_pizza.first())
                toppings = order.toppings.all()
                for topping in toppings:
                    inside_list.append(topping.topping)

                orders_list_pizza.append(inside_list)

            elif order.type == "subs":
                total += order.order_subs.first().price


                inside_list.append(order.order_subs.first())
                addons = order.addons.all()
                for addon in addons:

                    inside_list.append(addon.flavor)
                    total += addon.price

                orders_list_subs.append(inside_list)

            elif order.type =="pasta":

                total += order.order_pasta.first().price

                orders_list_pasta.append(order.order_pasta.first())

            elif order.type == "salads":
                total += order.order_salads.first().price

                orders_list_salads.append(order.order_salads.first())

            elif order.type == "dinner":
                total += order.order_dinner.first().price

                orders_list_dinner.append(order.order_dinner.first())


    # total of the purchase to be presented to the customer and to be used on Stripe for credit card payment
    total = round(total, 2)
    total_stripe = int(total*100)
    key = os.getenv("STRIPE_API")

    context = {
        "message": "",
        "user": user,
        "orders_list_pizza": orders_list_pizza,
        "orders_list_subs": orders_list_subs,
        "orders_list_pasta": orders_list_pasta,
        "orders_list_salads": orders_list_salads,
        "orders_list_dinner": orders_list_dinner,
        "total": total,
        "total_stripe": total_stripe,
        "orders": orders,
        "key": key
    }
    return render(request, "users/shopping_cart.html", context)

def confirmed_order(request):
    """if order is confirmed, add shopping cart order to placed orders. Delete from shopping cart if otherwise """
    confirmed = request.POST["confirmed"]
    if confirmed == "Confirm":
        user = request.user
        orders = Shopping_Cart.objects.filter(user=user)
        for order in orders:
            if not order.confirmed:
                placed_orders = Placed_Orders(placed_order=order)
                placed_orders.save()
        orders.update(confirmed=True)
        context = {
            "message": "Your order was placed!"
        }

    else:
        user = request.user
        orders = Shopping_Cart.objects.filter(user=user)
        for order in orders:
            if not order.confirmed:
                order.delete()
        context = {
            "message": "Your order was canceled!"
        }

    return render(request, "users/shopping_cart.html", context)

def confirmed_order_pay(request):
    """use credit card with Stripe, update shopping card order to confirmed and send email to customer using EmailMessage"""
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = os.getenv("STRIPE_API2")

    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    token = request.POST['stripeToken']

    charge = stripe.Charge.create(
        amount=999,
        currency='usd',
        description='Example charge',
        source=token,
    )

    user = request.user
    orders = Shopping_Cart.objects.filter(user=user)
    for order in orders:
        if not order.confirmed:
            placed_orders = Placed_Orders(placed_order=order)
            placed_orders.save()
    orders.update(confirmed=True)

    context = {
        "message": "Your order was placed!"
    }

    email = EmailMessage('Your Order on Pinnochio Pizza', 'Your order was placed!', to=[user.email])
    email.send()

    return render(request, "users/shopping_cart.html", context)



