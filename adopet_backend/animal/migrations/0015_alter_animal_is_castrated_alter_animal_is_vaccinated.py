# Generated by Django 5.0.3 on 2024-04-23 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animal", "0014_animal_is_castrated_animal_is_vaccinated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="is_castrated",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="animal",
            name="is_vaccinated",
            field=models.BooleanField(),
        ),
    ]
