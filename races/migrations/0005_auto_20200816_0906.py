from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("races", "0004_race_background"),
    ]

    operations = [
        migrations.AlterField(
            model_name="racer",
            name="trailhawk",
            field=models.OneToOneField(
                null=True,
                blank=True,
                to="members.Member",
                on_delete=models.CASCADE,
                help_text="If racer is a trailhawk select profile.",
            ),
        ),
    ]
