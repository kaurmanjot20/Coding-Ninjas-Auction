# Generated by Django 5.0.4 on 2024-04-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player_Groups',
            fields=[
                ('group_id', models.IntegerField(primary_key=True, serialize=False)),
                ('group_price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Individual',
            fields=[
                ('player_id', models.IntegerField(primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=50)),
                ('player_price', models.FloatField(default=0.0)),
            ],
        ),
    ]