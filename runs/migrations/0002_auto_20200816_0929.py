from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("runs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="run",
            name="enable_comments",
            field=models.BooleanField(default=False),
        ),
    ]
