# Generated by Django 3.0.14 on 2021-06-12 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0004_remove_event_enable_comments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="body",
            field=models.TextField(blank=True),
        ),
    ]
