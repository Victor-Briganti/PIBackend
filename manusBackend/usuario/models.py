from django.db import models

# Create your models here.


class Endereco(models.Model):
    cep = models.CharField(("CEP"), max_length=9)
    logradouro = models.CharField(("Logradouro"), max_length=200)
    bairro = models.CharField(("Bairro"), max_length=200)
    numero = models.CharField(("Numero"), max_length=10)
    complemento = models.CharField(("Complemento"), max_length=100)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}"


class Usuario(models.Model):
    """
    Classe do Usuário.
    TODO: Dividir usuário em comum e administrador
    """

    cpf = models.CharField(("CPF"), max_length=14, primary_key=True)
    nome = models.CharField(("Nome"), max_length=200)
    senha = models.CharField(("Senha"), max_length=20)
    email = models.CharField(("Email"), max_length=200)
    telefone = models.CharField(("Telefone"), max_length=13)
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return str(self.cpf)
