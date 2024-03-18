from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    """
    Configuração da aplicação de usuários.

    default_auto_field: Define o tipo de chave primária padrão.
    name: Define o nome da aplicação.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "usuario"
