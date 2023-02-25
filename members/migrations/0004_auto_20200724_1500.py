from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0003_remove_member_gender"),
    ]

    operations = [
        migrations.RenameField(
            model_name="member",
            old_name="gender_text",
            new_name="gender",
        ),
    ]
