from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile


def home(req):
    return render(req,'home.html')


def sign(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if len(phone) != 10:
            messages.error(request, "Enter valid 10 digit mobile number")
            return redirect("sign")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("sign")

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Mobile number already registered")
            return redirect("sign")

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Save phone
        Profile.objects.create(user=user, phone=phone)

        messages.success(request, "Account Created Successfully")
        return redirect("login")

    return render(request, "signup.html")