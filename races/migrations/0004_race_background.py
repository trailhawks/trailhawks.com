from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flickr", "0002_photo_active"),
        ("races", "0003_remove_race_background"),
    ]

    operations = [
        migrations.AddField(
            model_name="race",
            name="background",
            field=models.ForeignKey(
                blank=True, to="flickr.Photo", on_delete=models.CASCADE, null=True
            ),
            preserve_default=True,
        ),
    ]
