from django.shortcuts import render
from OJ.helper import Helper

# Create your views here.
def index(request):
    return render(request, "index.html", {'background_class': Helper().get_background_class()})

def problemset(request):
    return render(request, "problemset.html", {'background_class': Helper().get_background_class()})
