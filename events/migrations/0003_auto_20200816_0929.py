# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_event_races"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="enable_comments",
            field=models.BooleanField(default=False),
        ),
    ]
