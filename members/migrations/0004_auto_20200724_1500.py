# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_remove_member_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='gender_text',
            new_name='gender',
        ),
    ]
