# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0006_auto_20200816_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='enable_comments',
        ),
    ]
