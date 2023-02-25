from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="gender_text",
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
