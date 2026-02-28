from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0024_migrate_racer_gender_to_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="racer",
            name="gender",
        ),
    ]
