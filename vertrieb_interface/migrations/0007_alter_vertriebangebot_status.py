# Generated by Django 4.2.2 on 2023-06-18 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vertrieb_interface", "0006_alter_vertriebangebot_status"),
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
                    ("on Hold", "on Hold"),
                    ("storniert", "storniert"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]