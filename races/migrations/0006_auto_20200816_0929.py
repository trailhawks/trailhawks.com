# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0005_auto_20200816_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='enable_comments',
            field=models.BooleanField(default=False),
        ),
    ]
