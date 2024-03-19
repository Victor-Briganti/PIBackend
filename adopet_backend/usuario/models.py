from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UsuarioManager(BaseUserManager):
    """
    Gerenciador de usuário para o modelo de usuário customizado.
    Necessário para criar usuários com o modelo de usuário customizado.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email é um campo obrigatório")

        if not password:
            raise ValueError("Senha é campo obrigatória")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário customizado.
    Usado para extender a classe de usuário padrão do Django.
    """

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    # Campo usado para desativar usuários
    is_active = models.BooleanField(default=True)
    # Determina se o usuário tem acesso ao painel de administração
    is_staff = models.BooleanField(default=False)

    # Sobrescreve o campo objects com um outro gerenciador de usuário
    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get \
                   all permissions granted to each of their groups.",
        related_name="usuario_groups",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="usuario_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        return str(self.email)
