"""
Funções de validação para os campos do modelo Usuário.
"""

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

# Salva o modelo de usuário atual em uma váriavel.
# Definido em "AUTH_USER_MODEL"
UserModel = get_user_model()


def validate_user(validated_data):
    """
    Valida os todo os campos para um novo usuário.
    """
    email = validated_data["email"].strip()
    firstname = validated_data["firstname"].strip()
    lastname = validated_data["lastname"].strip()
    password = validated_data["password"].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError("O email já está em uso ou é inválido.")

    if not password or len(password) < 8:
        raise ValidationError("A senha é inválida.")

    if not firstname:
        raise ValidationError("Primeiro nome é inválido.")

    if not lastname:
        raise ValidationError("Último nome é inválido.")

    return validated_data


def validate_email(data):
    email = data["email"].strip()

    if not email:
        raise ValidationError("Um email é necessário.")

    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        raise ValidationError("O email é inválido.")

    return True


def validate_password(data):
    password = data["password"].strip()

    if not password:
        raise ValidationError("Uma senha é necessária.")

    if len(password) < 8:
        raise ValidationError("A senha deve ter pelo menos 8 caracteres.")

    return True
