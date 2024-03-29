# Generated by Django 3.2.18 on 2023-03-08 23:36

import ajaximage.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("flickr", "0006_photo_tags"),
        ("races", "0019_series"),
    ]

    operations = [
        migrations.AlterField(
            model_name="race",
            name="background",
            field=models.ForeignKey(
                blank=True,
                help_text="The background image is used on the homepage.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="flickr.photo",
            ),
        ),
        migrations.AlterField(
            model_name="race",
            name="logo",
            field=ajaximage.fields.AjaxImageField(
                blank=True,
                help_text="The logo image is on the top of the race page.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="race",
            name="race_type",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "Run"), (2, "Bike"), (3, "Swim")],
                default=1,
                null=True,
            ),
        ),
    ]
