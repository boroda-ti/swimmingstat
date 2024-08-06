from django.db import models

from user_app.models import Athlete

STYLES_CHOICES = [
    ('fr', 'Вільний стиль'),
    ('bk', 'На спині'),
    ('br', 'Брас'),
    ('bt', 'Батерфляй'),
    ('im', 'Комплекс'),
]

DISTANCE_CHOICES = [
    ('25m', '25 метрів'),
    ('50m', '50 метрів'),
    ('100m', '100 метрів'),
    ('200m', '200 метрів'),
    ('400m', '400 метрів'),
    ('800m', '800 метрів'),
    ('1500m', '1500 метрів'),

    # Additional distances
    ('1k', '1 кілометр'),
    ('1250m', '1250 метрів'),
    ('2k', '2 кілометра'),
    ('2.5k', '2,5 кілометра'),
    ('5k', '5 кілометрів'),
    ('7.5k', '7,5 кілометрів'),
    ('10k', '10 кілометрів'),
]

class Competitions(models.Model):

    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    date_begin = models.DateField()
    date_end = models.DateField()

    # check end date >= begin date

class Result(models.Model):

    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    
    style = models.CharField(max_length=2, choices=STYLES_CHOICES)
    distance = models.CharField(max_length=5, choices=DISTANCE_CHOICES)

    time = models.TimeField()

class DistanceToDay(models.Model):

    competitions = models.ForeignKey(Competitions, on_delete=models.CASCADE)

    style = models.CharField(max_length=2, choices=STYLES_CHOICES)
    distance = models.CharField(max_length=5, choices=DISTANCE_CHOICES)

    day = models.DateField()
    order = models.PositiveSmallIntegerField(default=1)

    # check if day between competition begin end datas