# Generated by Django 4.2.2 on 2023-06-17 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ElectricInvoice",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "invoice_id",
                    models.CharField(default=None, max_length=255, unique=True),
                ),
                ("current_date", models.DateField(auto_now_add=True)),
                ("is_locked", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Position",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "position",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "Hauptleitungsabzweigklemmen 35mm",
                                "Hauptleitungsabzweigklemmen 35mm",
                            ),
                            ("Kabelschellen Metall", "Kabelschellen Metall"),
                            ("Kabelkanal 10x60mm", "Kabelkanal 10x60mm"),
                            ("Kabelkanal 30x30mm", "Kabelkanal 30x30mm"),
                            ("Kabelkanal 60x60mm", "Kabelkanal 60x60mm"),
                            (
                                "Mantellleitung NYY-J 5x16qmm",
                                "Mantellleitung NYY-J 5x16qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x16qmm",
                                "Mantellleitung NYM-J 5x16qmm",
                            ),
                            (
                                "Mantellleitung NYY-J 1x16qmm",
                                "Mantellleitung NYY-J 1x16qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 1x16qmm",
                                "Mantellleitung NYM-J 1x16qmm",
                            ),
                            (
                                "Mantellleitung NYY-J 5x10qmm",
                                "Mantellleitung NYY-J 5x10qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x10qmm",
                                "Mantellleitung NYM-J 5x10qmm",
                            ),
                            (
                                "Mantellleitung NYY-J 5x6qmm",
                                "Mantellleitung NYY-J 5x6qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x6qmm",
                                "Mantellleitung NYM-J 5x6qmm",
                            ),
                            (
                                "Mantellleitung NYY-J 5x4qmm",
                                "Mantellleitung NYY-J 5x4qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x4qmm",
                                "Mantellleitung NYM-J 5x4qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x2.5qmm",
                                "Mantellleitung NYM-J 5x2.5qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 3x2.5qmm",
                                "Mantellleitung NYM-J 3x2.5qmm",
                            ),
                            (
                                "Mantellleitung NYM-J 5x1.5qmm",
                                "Mantellleitung NYM-J 5x1.5qmm",
                            ),
                            ("H07-VK 16mm² sw", "H07-VK 16mm² sw"),
                            ("H07-VK 16mm² bl", "H07-VK 16mm² bl"),
                            ("H07-VK 16mm² gn/ge", "H07-VK 16mm² gn/ge"),
                            ("H07-VK 10mm² sw", "H07-VK 10mm² sw"),
                            ("H07-VK 10mm² bl", "H07-VK 10mm² bl"),
                            ("H07-VK 10mm² gn/ge", "H07-VK 10mm² gn/ge"),
                            ("H07-VK 4mm² sw", "H07-VK 4mm² sw"),
                            ("H07-VK 4mm² bl", "H07-VK 4mm² bl"),
                            ("H07-VK 4mm² gn/ge", "H07-VK 4mm² gn/ge"),
                            ("H07-VK 2.5mm² sw", "H07-VK 2.5mm² sw"),
                            ("H07-VK 2.5mm² bl", "H07-VK 2.5mm² bl"),
                            ("H07-VK 2.5mm² gn/ge", "H07-VK 2.5mm² gn/ge"),
                            (
                                "Leitungsschutzschalter 3polig B16",
                                "Leitungsschutzschalter 3polig B16",
                            ),
                            (
                                "Leitungsschutzschalter 3polig B20",
                                "Leitungsschutzschalter 3polig B20",
                            ),
                            (
                                "Leitungsschutzschalter 3polig B25",
                                "Leitungsschutzschalter 3polig B25",
                            ),
                            (
                                "Leitungsschutzschalter 3polig B32",
                                "Leitungsschutzschalter 3polig B32",
                            ),
                            (
                                "Leitungsschutzschalter 3polig B40",
                                "Leitungsschutzschalter 3polig B40",
                            ),
                            (
                                "Leitungsschutzschalter 1polig B10",
                                "Leitungsschutzschalter 1polig B10",
                            ),
                            (
                                "Leitungsschutzschalter 1polig B16",
                                "Leitungsschutzschalter 1polig B16",
                            ),
                            (
                                "Leitungsschutzschalter 1polig B20",
                                "Leitungsschutzschalter 1polig B20",
                            ),
                            (
                                "Leitungsschutzschalter 1polig B25",
                                "Leitungsschutzschalter 1polig B25",
                            ),
                            ("SLS  3polig E35A", "SLS  3polig E35A"),
                            ("SLS  3polig E50A", "SLS  3polig E50A"),
                            ("SLS  3polig E63A", "SLS  3polig E63A"),
                            (
                                "Überspannungsschutz (Kombiableiter Phasenschiene)",
                                "Überspannungsschutz (Kombiableiter Phasenschiene)",
                            ),
                            (
                                "Überspannungsschutz (Kombiableiter Hutschiene)",
                                "Überspannungsschutz (Kombiableiter Hutschiene)",
                            ),
                            ("Hauptschalter 3x63A", "Hauptschalter 3x63A"),
                            (
                                "Fehlerstromschutzschalter 4polig 40A/30mA",
                                "Fehlerstromschutzschalter 4polig 40A/30mA",
                            ),
                            ("FI/LS 2polig 16A/30mA", "FI/LS 2polig 16A/30mA"),
                            ("FI/LS 2polig 25A/30mA", "FI/LS 2polig 25A/30mA"),
                            ("FI/LS 4polig 16A/30mA", "FI/LS 4polig 16A/30mA"),
                            ("FI/LS 4polig 25A/30mA", "FI/LS 4polig 25A/30mA"),
                            ("Kammschiene 3phasig", "Kammschiene 3phasig"),
                            ("Kammschiene 3phasig (N)", "Kammschiene 3phasig (N)"),
                            (
                                "Phoenixkontakt-Klemmen PE/L/NT",
                                "Phoenixkontakt-Klemmen PE/L/NT",
                            ),
                            (
                                "Phoenixkontakt-Klemmen L/L",
                                "Phoenixkontakt-Klemmen L/L",
                            ),
                            (
                                "Phoenixkontakt-Einspeiseklemme N",
                                "Phoenixkontakt-Einspeiseklemme N",
                            ),
                            ("Kupferschiene N", "Kupferschiene N"),
                            (
                                "Phoenixkontakt-Einspeiseklemme N Seitendeckel",
                                "Phoenixkontakt-Einspeiseklemme N Seitendeckel",
                            ),
                            (
                                "Phoenixkontakt-Stufenklemmen",
                                "Phoenixkontakt-Stufenklemmen",
                            ),
                            (
                                "Phoenixkontakt-Klemmen Seitendeckel grau",
                                "Phoenixkontakt-Klemmen Seitendeckel grau",
                            ),
                            ("Endkappen Kammschiene", "Endkappen Kammschiene"),
                            (
                                "Berührungsschutz Kammschiene",
                                "Berührungsschutz Kammschiene",
                            ),
                            ("Klemmblock Hutschiene N", "Klemmblock Hutschiene N"),
                            ("Klemmblock Hutschiene PE", "Klemmblock Hutschiene PE"),
                            (
                                "Installationsklemmen (-4mm²)",
                                "Installationsklemmen (-4mm²)",
                            ),
                            (
                                "Installationsklemmen (-6mm²)",
                                "Installationsklemmen (-6mm²)",
                            ),
                            (
                                "Installationsklemmen (-10mm²)",
                                "Installationsklemmen (-10mm²)",
                            ),
                            (
                                "Hutschienenhalter Installationsklemmen",
                                "Hutschienenhalter Installationsklemmen",
                            ),
                            ("Aufputz-Abzweigdosen", "Aufputz-Abzweigdosen"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("quantity", models.FloatField(blank=True, null=True)),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="positions",
                        to="invoices.electricinvoice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KundenData",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "kunden_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "kunden_strasse",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "kunden_plz_ort",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("standort", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "zahlerschranken",
                    models.CharField(
                        choices=[
                            ("1-Zähler-Anlagen", "1-Zähler-Anlagen"),
                            ("2-Zähler-Anlagen", "2-Zähler-Anlagen"),
                            ("3-Zähler-Anlagen", "3-Zähler-Anlagen"),
                            ("4-Zähler-Anlagen", "4-Zähler-Anlagen"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "netz_typ",
                    models.CharField(
                        choices=[
                            ("-TN-S-Netz", "-TN-S-Netz"),
                            ("-TN-C-Netz", "-TN-C-Netz"),
                            ("-TW-C-S-Netz", "-TW-C-S-Netz"),
                            ("-TT-Netz", "-TT-Netz"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "invoice",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kunden_data",
                        to="invoices.electricinvoice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
