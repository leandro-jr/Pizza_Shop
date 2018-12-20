from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shopping_cart", views.shopping_cart, name="shopping_cart"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("order_pizza", views.order_pizza, name="order_pizza"),
    path("order_subs", views.order_subs, name="order_subs"),
    path("order_pasta", views.order_pasta, name="order_pasta"),
    path("order_salads", views.order_salads, name="order_salads"),
    path("order_dinner", views.order_dinner, name="order_dinner"),
    path("order_toppings", views.order_toppings, name="order_toppings"),
    path("order_addon", views.order_addon, name="order_addon"),
    path("confirmed_order", views.confirmed_order, name="confirmed_order"),
    path("confirmed_order_pay", views.confirmed_order_pay, name="confirmed_order_pay")
]
