from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


class State(models.Model):
    """
    Modelo de Estado.
    """

    STATE_CHOICES = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )

    uf = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        validators=[MinLengthValidator(2), MaxLengthValidator(2)],
    )

    def __str__(self):
        state_dict = dict(self.STATE_CHOICES)
        return state_dict.get(self.uf, self.uf)


class City(models.Model):
    """
    Modelo de Cidade.
    """

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Address(models.Model):
    """
    Modelo de Endereço.
    """

    zip_code = models.CharField(
        max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)]
    )
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    complement = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return (
            "Logradouro: "
            + str(self.street)
            + ". Bairro: "
            + str(self.district)
            + ". Número: "
            + str(self.house_number)
            + ". CEP: "
            + str(self.zip_code)
        )
