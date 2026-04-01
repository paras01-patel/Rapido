from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile,Contact


def home(request):
    username = request.session.get('username')  # session se username le lo

    if not username:
        return redirect('login')  # agar login nahi hai

    return render(request, 'home.html', {"username": username})

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        # ✅ DATABASE SAVE
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')   # refresh issue avoid

    return render(request, 'contact.html')

# 📝 Signup
def sign(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # ❌ empty check
        if not username or not phone or not password:
            messages.error(request, "All fields are required")
            return redirect("sign")

        # ❌ phone check
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter valid 10 digit number")
            return redirect("sign")

        # ❌ username exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("sign")

        # ❌ phone exist
        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Mobile already registered")
            return redirect("sign")

        # ✅ create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ✅ save phone
        Profile.objects.create(user=user, phone=phone)

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "sign.html")


# 🔐 Login
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # empty check
        if not username or not password:
            return render(request, "login.html", {"error": "All fields required"})

        user = User.objects.filter(username=username).first()

        # check user + password
        if user and user.check_password(password):

            # 👉 SESSION LOGIN (manual)
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            return redirect('home')
        else:
            return render(request, "login.html", {"error": "Invalid details"})

    return render(request, "login.html")



def logout(request):
    request.session.flush()  # session clear
    return redirect('sign')