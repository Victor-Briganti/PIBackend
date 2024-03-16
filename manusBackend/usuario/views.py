from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Usuario
from .forms import UsuarioForm

# Create your views here.


def index(request):
    return render(request, "usuario/index.html")


def contato(request):
    return render(request, "usuario/contato.html")


def sobre(request):
    return render(request, "usuario/sobre.html")


def login_page(request):
    # Verifica se a requisição HTTP é um POST
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        # Verifica se o usuário existe
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return redirect("/login/")  # Continua na página de login

        # Verifica se a senha é válida
        if usuario.senha != senha:
            messages.error(request, "Senha inválida")
            return redirect("/login/")
        else:
            return redirect("sucesso")

    return render(request, "usuario/login.html")


def cadastro(request):
    # Verifica se a requisição HTTP é um POST
    if request.method == "POST":
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("sucesso")

        # Mostra todas mensagens de erro
        erros = form.errors.as_data()
        for campo, lista_erros in erros.items():
            for erro in lista_erros:
                messages.error(request, f"{campo}: {erro.message}")

    else:
        form = UsuarioForm()

    return render(request, "usuario/cadastro.html", {"form": form})


def sucesso(request):
    return render(request, "usuario/sucesso.html")
