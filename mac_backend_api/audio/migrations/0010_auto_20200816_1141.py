# Generated by Django 3.0.6 on 2020-08-16 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0009_auto_20200816_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audio',
            options={'permissions': (('change_own_audio', 'Can change own audio'), ('delete_own_audio', 'Can delete own audio'))},
        ),
        migrations.AlterModelOptions(
            name='stream',
            options={'permissions': (('change_own_stream', 'Can change own stream'), ('delete_own_stream', 'Can delete own stream'))},
        ),
    ]
