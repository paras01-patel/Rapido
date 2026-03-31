from django.shortcuts import render

# Create your views here.


def home(req):
    return render(req,'home.html')


def sign(req):
    return render (req,'sign.html')