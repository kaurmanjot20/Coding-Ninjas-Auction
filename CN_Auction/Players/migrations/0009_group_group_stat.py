# Generated by Django 5.0.4 on 2024-04-16 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Players', '0008_group_alloted_team_group_stat_wicketkeeper'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_stat',
            field=models.IntegerField(default=0),
        ),
    ]