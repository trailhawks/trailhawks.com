from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0002_member_gender_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="gender",
        ),
    ]
