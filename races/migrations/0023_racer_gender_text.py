from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0022_remove_race_background"),
    ]

    operations = [
        migrations.AddField(
            model_name="racer",
            name="gender_text",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
