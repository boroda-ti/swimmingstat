# Generated by Django 5.0.7 on 2024-08-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_customuser_initial_name_customuser_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='initial_name',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
