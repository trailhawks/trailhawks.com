from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0004_auto_20200724_1500"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="email",
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
