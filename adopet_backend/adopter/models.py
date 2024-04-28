from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from user.models import User
from address.models import Address
from animal.models import Animal

# Create your models here.


class Adopter(models.Model):
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(11),
        ],
    )
    birth_date = models.DateField()
    phone = models.CharField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(11),
        ],
    )
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Adoption(models.Model):
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="animal_registers"
    )
    staff = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="staff_registers"
    )
    register_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(null=True, blank=True)


class AnimalRegister(models.Model):
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="animal_registers"
    )
    staff = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="staff_registers"
    )
    register_date = models.DateTimeField(auto_now_add=True)
    request_status = models.CharField(null=True, blank=True)
