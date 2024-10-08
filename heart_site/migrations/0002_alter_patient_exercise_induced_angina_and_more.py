# Generated by Django 4.2.13 on 2024-07-07 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("heart_site", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="exercise_induced_angina",
            field=models.BooleanField(choices=[(False, "No"), (True, "Yes")]),
        ),
        migrations.AlterField(
            model_name="patient",
            name="fasting_blood_sugar_greater_than_120mgdl",
            field=models.BooleanField(choices=[(False, "No"), (True, "Yes")]),
        ),
    ]
