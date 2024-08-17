from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from .models import Athlete, Competitions, DistanceToDay

class AthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Athlete
        fields = '__all__'

class DistanceToDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = DistanceToDay
        fields = '__all__'

    def validate(self, data):
        competition = data.get('competitions')
        day = data.get('day')
        distance = data.get('distance')
        
        if not (competition.date_begin <= day <= competition.date_end):
            raise serializers.ValidationError(
                _(f"The day must be between {competition.date_begin} and {competition.date_end}.")
            )

        if DistanceToDay.objects.filter(
            competitions=competition, 
            distance=distance
        ).exclude(day=day).exists():
            raise serializers.ValidationError(
                _("This distance is already assigned to another day within the same competition.")
            )

        return data