# Generated by Django 5.0.3 on 2024-04-28 03:00

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("address", "__first__"),
        ("animal", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Adopter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cpf",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(11),
                            django.core.validators.MaxLengthValidator(11),
                        ],
                    ),
                ),
                ("birth_date", models.DateField()),
                (
                    "phone",
                    models.CharField(
                        max_length=11,
                        validators=[
                            django.core.validators.MinLengthValidator(11),
                            django.core.validators.MaxLengthValidator(11),
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="address.address",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Adoption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_date", models.DateTimeField(auto_now_add=True)),
                ("request_status", models.CharField(blank=True, null=True)),
                ("comments", models.TextField(blank=True, null=True)),
                (
                    "adopter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="adopter.adopter",
                    ),
                ),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="animal.animal"
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AnimalRegister",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("register_date", models.DateTimeField(auto_now_add=True)),
                ("request_status", models.CharField(blank=True, null=True)),
                (
                    "adopter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="adopter.adopter",
                    ),
                ),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="animal.animal"
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]