# Generated by Django 5.0.7 on 2024-08-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_app', '0010_remove_result_style_alter_result_distance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='distancetoday',
            name='athlete',
            field=models.ManyToManyField(to='stats_app.athlete'),
        ),
        migrations.DeleteModel(
            name='DistanceToDayAthletes',
        ),
    ]
