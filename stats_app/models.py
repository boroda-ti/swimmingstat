from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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

SEX_CHOICES = [
    ('m', 'Чоловіки'),
    ('f', 'Жінки')
]

class Athlete(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    initial_name = models.CharField(max_length=30, default='-')
    date_of_birth = models.DateField()

    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True, blank=True)
    coach = models.ForeignKey('user_app.CustomUser', limit_choices_to={"is_coach": True}, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}, coach : {self.coach}'


class School(models.Model):

    name = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Competitions(models.Model):

    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    date_begin = models.DateField()
    date_end = models.DateField()

    def clean(self):
        if self.date_begin > self.date_end:
            raise ValidationError(_('Competitions end date cant be less that begin date'))
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Distance(models.Model):

    style = models.CharField(max_length=2, choices=STYLES_CHOICES)
    distance = models.CharField(max_length=5, choices=DISTANCE_CHOICES)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    def __str__(self):
        return f'{self.distance} {self.style} {self.sex}'

class DistanceToDay(models.Model):

    competitions = models.ForeignKey(Competitions, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    athlete = models.ManyToManyField(Athlete)

    day = models.DateField()
    order = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['competitions', 'distance'],
                name='unique_distance_per_competition'
            ),  
            models.UniqueConstraint(
                fields=['competitions', 'day', 'order'],
                name='unique_order_per_day'
            )
        ]

    def clean(self):
        if not (self.competitions.date_begin <= self.day <= self.competitions.date_end):
            raise ValidationError(
                _(f"The day must be between {self.competitions.date_begin} and {self.competitions.date_end}.")
            )
        
        if DistanceToDay.objects.filter(
            competitions=self.competitions, 
            distance=self.distance
        ).exclude(day=self.day).exists():
            raise ValidationError(
                _("This distance is already assigned to another day within the same competition.")
            )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.competitions}, {self.day} : {self.distance} - {self.order}'

class Result(models.Model):
    competitions = models.ForeignKey(Competitions, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    time = models.TimeField()