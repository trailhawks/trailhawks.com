# Generated by Django 3.0.14 on 2021-06-12 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0011_auto_20210612_1045"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="racer",
            name="shirt_size",
        ),
    ]