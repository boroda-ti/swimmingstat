from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import Coach

class CoachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coach
        fields = ('email', 'password')

    password = serializers.CharField(write_only=True)