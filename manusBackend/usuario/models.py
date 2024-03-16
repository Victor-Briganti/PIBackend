from django.db import models

# Create your models here.

class Usuario(models.Model):
    '''
        Classe do Usuário.
        TODO: Criar modelo de endereços
        TODO: Dividi usuário em comum e administrador
    '''
    cpf = models.CharField(("CPF"), max_length=14, primary_key=True)
    nome = models.CharField(("Nome"), max_length=200, default="Teste")
    senha = models.CharField(("Senha"), max_length=20, default="1234")
    email = models.CharField(("Email"), max_length=200)
    telefone = models.CharField(("Telefone"), max_length=13)

    def __str__(self):
        return str(self.cpf)
