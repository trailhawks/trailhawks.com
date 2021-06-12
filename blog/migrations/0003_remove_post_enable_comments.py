from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_auto_20200816_0929"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="enable_comments",
        ),
    ]
