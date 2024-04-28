# Generated by Django 5.0.3 on 2024-04-28 03:00

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Animal",
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
                ("name", models.CharField(max_length=100)),
                (
                    "age",
                    models.CharField(
                        choices=[
                            ("puppy", "Filhote"),
                            ("adult", "Adulto"),
                            ("old", "Idoso"),
                        ]
                    ),
                ),
                (
                    "specie",
                    models.CharField(choices=[("dog", "Cachorro"), ("cat", "Gato")]),
                ),
                ("gender", models.CharField(choices=[("M", "Macho"), ("F", "Fêmea")])),
                (
                    "size",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("small", "Pequeno porte"),
                            ("medium", "Médio porte"),
                            ("large", "Grande porte"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("temperament", models.CharField(blank=True, null=True)),
                (
                    "coat",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("short", "Curto"),
                            ("medium", "Médio"),
                            ("long", "Longo"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "weight",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("adoption_date", models.DateTimeField(blank=True, null=True)),
                ("register_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_house_trained", models.BooleanField()),
                ("is_special_needs", models.BooleanField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_vaccinated", models.BooleanField()),
                ("is_castrated", models.BooleanField()),
                ("is_adopted", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="ImageAnimal",
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
                ("image", models.ImageField(default="", upload_to="image/animals/")),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="animal.animal"
                    ),
                ),
            ],
        ),
    ]
