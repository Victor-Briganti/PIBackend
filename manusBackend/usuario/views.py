from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "usuario/index.html")

def contato(request):
    return render(request, "usuario/contato.html")

def sobre(request):
    return render(request, "usuario/sobre.html")
