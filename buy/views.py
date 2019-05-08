from django.shortcuts import render

# Create your views here.
def cart(req):
    return render(req,"cart.html")