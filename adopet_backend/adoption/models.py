from django.db import models
from user.models import User
from address.models import Address
from animal.models import Animal

# Create your models here.

STATUS_CHOICES = [
    ("approved", "Aprovado"),
    ("rejected", "Rejeitado"),
    ("pending", "Pendente"),
]


class Adoption(models.Model):
    donor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="adoptions_as_donor"
    )
    adopter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="adoptions_as_adopter"
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    request_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", null=True, blank=True
    )
    comments = models.TextField(null=True, blank=True)
