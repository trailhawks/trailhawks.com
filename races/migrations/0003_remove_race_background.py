from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("races", "0002_race_sponsors"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="race",
            name="background",
        ),
    ]
