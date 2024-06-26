# Generated by Django 5.0.3 on 2024-04-30 20:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("address", "__first__"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("firstname", models.CharField(max_length=100)),
                ("lastname", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, default="", null=True, upload_to="image/avatar/"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Grupo que este usuário pertece. Um usuário irá conseguir todas as permissões de seu grupo.",
                        related_name="user_groups",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Especifica as permissões de usuário.",
                        related_name="user_user_permissions",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserMetadata",
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
    ]
