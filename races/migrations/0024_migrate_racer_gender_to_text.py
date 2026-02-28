from django.db import migrations


GENDER_MAP = {
    1: "Man",
    2: "Woman",
}


def forwards(apps, schema_editor):
    Racer = apps.get_model("races", "Racer")
    for racer in Racer.objects.all():
        racer.gender_text = GENDER_MAP.get(racer.gender, "")
        racer.save(update_fields=["gender_text"])


def backwards(apps, schema_editor):
    REVERSE_MAP = {v: k for k, v in GENDER_MAP.items()}
    Racer = apps.get_model("races", "Racer")
    for racer in Racer.objects.all():
        racer.gender = REVERSE_MAP.get(racer.gender_text, 1)
        racer.save(update_fields=["gender"])


class Migration(migrations.Migration):

    dependencies = [
        ("races", "0023_racer_gender_text"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
