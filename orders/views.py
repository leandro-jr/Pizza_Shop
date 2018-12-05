from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
# def index(request):
#     return HttpResponse("Project 3: TODO")

def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "users/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def register_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    if password == confirm_password:
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name )
        return render(request, "users/login.html", {"message": "None"})
    else:
        return render(request, "users/login.html", {"message": "Passwords do not match."})




