# Generated by Django 5.0.4 on 2024-04-16 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0006_rename_player_group_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='player_img',
        ),
    ]
