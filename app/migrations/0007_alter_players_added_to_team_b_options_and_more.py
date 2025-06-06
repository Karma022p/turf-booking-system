# Generated by Django 5.1 on 2025-04-23 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_players_added_to_team_a_team_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='players_added_to_team_b',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='players_added_to_team_b',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='players_added_to_team_b',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teamb'),
        ),
    ]
