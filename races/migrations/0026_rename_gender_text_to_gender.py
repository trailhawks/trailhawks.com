from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0025_remove_racer_gender"),
    ]

    operations = [
        migrations.RenameField(
            model_name="racer",
            old_name="gender_text",
            new_name="gender",
        ),
    ]
