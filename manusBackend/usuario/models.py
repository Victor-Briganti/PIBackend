from django.db import models

# Create your models here.

class Usuario(models.Model):
    '''
        Classe do Usuário.
        TODO: Criar modelo de endereços
        TODO: Dividi usuário em comum e administrador
    '''
    cpf = models.CharField(("CPF"), max_length=11, primary_key=True)
    email = models.CharField(("Email"), max_length=200)
    telefone = models.CharField(("Telefone"), max_length=11)
