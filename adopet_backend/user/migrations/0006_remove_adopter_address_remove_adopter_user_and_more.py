# Generated by Django 5.0.3 on 2024-04-27 23:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_remove_user_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="adopter",
            name="address",
        ),
        migrations.RemoveField(
            model_name="adopter",
            name="user",
        ),
        migrations.DeleteModel(
            name="Address",
        ),
        migrations.DeleteModel(
            name="Adopter",
        ),
    ]
