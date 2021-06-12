from django.db import models, migrations


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
