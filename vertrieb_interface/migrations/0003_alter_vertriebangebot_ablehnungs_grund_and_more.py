# Generated by Django 4.2.2 on 2023-06-18 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vertrieb_interface", "0002_alter_vertriebangebot_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vertriebangebot",
            name="ablehnungs_grund",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "Abweichende Kundenvorstellung zum Thema PVA",
                        "Kundenvorstellung zum Thema PVA unterscheidet sich",
                    ),
                    ("Gebäude ungeeignet", "Das Gebäude ist nicht geeignet"),
                    (
                        "Günstigerer Mitbewerber",
                        "Ein Konkurrent bietet günstigere Optionen",
                    ),
                    (
                        "Investition lohnt sich nicht",
                        "Eine Investition lohnt sich nicht",
                    ),
                    ("Investition zu teuer", "Die Investitionskosten sind zu hoch"),
                    (
                        "Kunde hat kein Interesse mehr",
                        "Der Kunde hat kein Interesse mehr",
                    ),
                    ("Kunde ist zu alt", "Der Kunde ist nicht mehr interessiert"),
                    (
                        "Kunde möchte 3-phasige Notstromversorgung",
                        "Der Kunde benötigt eine 3-phasige Notstromversorgung",
                    ),
                    (
                        "Kunde möchte deutsche Produkte",
                        "Der Kunde bevorzugt deutsche Produkte",
                    ),
                    (
                        "Kunde möchte erst später bauen",
                        "Der Kunde möchte zu einem späteren Zeitpunkt bauen",
                    ),
                    (
                        "Kunde möchte Förderung abwarten",
                        "Der Kunde möchte auf Fördermittel warten",
                    ),
                    (
                        "Kunde möchte lokalen Ansprechpartner",
                        "Der Kunde wünscht einen Ansprechpartner vor Ort",
                    ),
                    (
                        "Kunde möchte PVA nur mieten",
                        "Der Kunde möchte die PVA-Anlage nur mieten",
                    ),
                    ("Kunde war nicht erreichbar", "Der Kunde war nicht erreichbar"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vertriebangebot",
            name="leadstatus",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ausstehend", "ausstehend"),
                    ("reklamiert", "reklamiert"),
                    ("akzeptiert", "akzeptiert"),
                    ("abgelehnt", "abgelehnt"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
