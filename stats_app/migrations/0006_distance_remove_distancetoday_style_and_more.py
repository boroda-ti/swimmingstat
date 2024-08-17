# Generated by Django 5.0.7 on 2024-08-12 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_app', '0005_alter_distancetoday_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(choices=[('fr', 'Вільний стиль'), ('bk', 'На спині'), ('br', 'Брас'), ('bt', 'Батерфляй'), ('im', 'Комплекс')], max_length=2)),
                ('distance', models.CharField(choices=[('25m', '25 метрів'), ('50m', '50 метрів'), ('100m', '100 метрів'), ('200m', '200 метрів'), ('400m', '400 метрів'), ('800m', '800 метрів'), ('1500m', '1500 метрів'), ('1k', '1 кілометр'), ('1250m', '1250 метрів'), ('2k', '2 кілометра'), ('2.5k', '2,5 кілометра'), ('5k', '5 кілометрів'), ('7.5k', '7,5 кілометрів'), ('10k', '10 кілометрів')], max_length=5)),
                ('sex', models.CharField(choices=[('m', 'Чоловіки'), ('f', 'Жінки')], max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='distancetoday',
            name='style',
        ),
        migrations.AlterField(
            model_name='distancetoday',
            name='distance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats_app.distance'),
        ),
    ]
