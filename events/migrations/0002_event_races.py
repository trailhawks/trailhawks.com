from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0001_initial"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="races",
            field=models.ManyToManyField(related_name="events", to="races.Race"),
            preserve_default=True,
        ),
    ]
