from django.db import models

# Create your models here.


class Usuario(models.Model):
    """
    Classe que representa um usuário do sistema

    Todos usuários do sistema devem ser cadastrados nessa classe.
    Somente usuários administradores podem cadastrar novos animais e realizar postagens.
    """

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    administrador = models.BooleanField(default=False)

    def __str__(self):
        return self.nome + ' ' + self.sobrenome
