"""
Funções de validação para os campos do modelo Usuário.
"""

from django.core.exceptions import ValidationError

from .models import Animal, TemperamentAnimal

INVALID_TEMPERAMENT_COMBINATIONS = [
    {"aggressive", "friendly"},
    {"aggressive", "affectionate"},
    {"aggressive", "friendly"},
    {"aggressive", "calm"},
    {"aggressive", "playful"},
    {"calm", "energetic"},
    {"playful", "shy"},
    {"shy", "sociable"},
    {"sociable", "territorial"},
]

def validate_temperament(validated_data):
    """
    Valida os tipos de temperamento de um animal.
    """
    temperaments = set(t["name"] for t in validated_data)

    for invalid_combination in INVALID_TEMPERAMENT_COMBINATIONS:
        if invalid_combination.issubset(temperaments):
            raise ValidationError(
                f"Combinação de temperamentos inválida.: {invalid_combination}"
            )

    return validated_data
