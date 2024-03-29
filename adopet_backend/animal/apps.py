from django.apps import AppConfig


class AnimalConfig(AppConfig):
    """
    Classe de configuração do app animal.
    name: Nome do app.
    default_auto_field: Define o tipo da chave primária padrão.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "animal"
