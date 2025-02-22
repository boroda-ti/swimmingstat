# Generated by Django 5.0.7 on 2024-08-13 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_app', '0009_distancetoday_unique_order_per_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='style',
        ),
        migrations.AlterField(
            model_name='result',
            name='distance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats_app.distance'),
        ),
        migrations.CreateModel(
            name='DistanceToDayAthletes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats_app.athlete')),
                ('distancetoday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats_app.distancetoday')),
            ],
        ),
    ]
