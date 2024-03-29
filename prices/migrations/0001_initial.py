# Generated by Django 4.2.2 on 2023-06-17 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AndereKonfigurationWerte",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="ElektrikPreis",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("actual_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("old_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="ModuleGarantiePreise",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("actual_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("old_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="ModulePreise",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("actual_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("old_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="OptionalAccessoriesPreise",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("actual_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("old_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="WallBoxPreise",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("actual_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("old_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Prices",
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
                    "andere_preise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.anderekonfigurationwerte",
                    ),
                ),
                (
                    "elektrik_prices",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.elektrikpreis",
                    ),
                ),
                (
                    "modul_garantie_preise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.modulegarantiepreise",
                    ),
                ),
                (
                    "modul_prices",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.modulepreise",
                    ),
                ),
                (
                    "optional_accessories_prices",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.optionalaccessoriespreise",
                    ),
                ),
                (
                    "wallbox_prices",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="prices.wallboxpreise",
                    ),
                ),
            ],
        ),
    ]
