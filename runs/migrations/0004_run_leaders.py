# Generated by Django 4.2.11 on 2024-04-16 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20200815_2351'),
        ('runs', '0003_remove_run_enable_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='leaders',
            field=models.ManyToManyField(blank=True, related_name='runs', to='members.member'),
        ),
    ]