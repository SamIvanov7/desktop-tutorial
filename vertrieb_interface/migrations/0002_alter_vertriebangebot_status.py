# Generated by Django 4.2.2 on 2023-06-17 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vertrieb_interface", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vertriebangebot",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("angenommen", "angenommen"),
                    ("bekommen", "bekommen"),
                    ("in Kontakt", "in Kontakt"),
                    ("Kontaktversuch", "Kontaktversuch"),
                    ("abgelehnt", "abgelehnt"),
                    ("abgelaufen", "abgelaufen"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
