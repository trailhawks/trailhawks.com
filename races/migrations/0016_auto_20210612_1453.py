# Generated by Django 3.0.14 on 2021-06-12 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("races", "0015_auto_20210612_1405"),
    ]

    operations = [
        migrations.AlterField(
            model_name="racer",
            name="gender",
            field=models.IntegerField(choices=[(1, "Man"), (2, "Woman")]),
        ),
        migrations.AlterField(
            model_name="result",
            name="place",
            field=models.TextField(
                blank=True,
                help_text="Ex. First Overall Man or First Masters Woman",
                null=True,
            ),
        ),
    ]
