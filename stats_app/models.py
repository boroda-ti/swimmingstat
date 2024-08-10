from django.db import models

RANK_CHOICES = [
        ('3Y', '3 юнацький'),
        ('2Y', '2 юнацький'),
        ('1Y', '1 юнацький'),
        ('3A', '3 дорослий'),
        ('2A', '2 дорослий'),
        ('1A', '1 дорослий'),
        ('CMS', 'КМС'),
        ('MS', 'МС'),
        ('MSMK', 'МСМК'),
    ]

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

class Athlete(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()

    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True, blank=True)
    coach = models.ForeignKey('user_app.CustomUser', limit_choices_to={"is_coach": True}, on_delete=models.SET_NULL, null=True, blank=True)


class School(models.Model):

    name = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

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