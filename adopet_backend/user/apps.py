from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Classe de configuração do app user.
    name: Nome do app.
    default_auto_field: Define o tipo da chave primária padrão.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
