# Generated by Django 4.2.2 on 2023-06-19 02:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0004_alter_user_sonstiges"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="zoho_data",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]