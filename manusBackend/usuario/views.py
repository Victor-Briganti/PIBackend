from django.shortcuts import render
from .models import Usuario
# Create your views here.

def index(request):
    return render(request, "usuario/index.html")

def contato(request):
    return render(request, "usuario/contato.html")

def sobre(request):
    return render(request, "usuario/sobre.html")

def create_view(request):
    return render(request,"usuario/create_view.html")
