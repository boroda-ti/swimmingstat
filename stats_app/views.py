from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from user_app.permissions import IsCoachOrStaff

from .models import Athlete
from .serializers import AthleteSerializer

class AthleteCRUDAPIView(APIView):

    permission_classes = [IsCoachOrStaff]

    def get(self, request, pk=None):
        if pk:
            athlete = get_object_or_404(Athlete, pk=pk)
            serializer = AthleteSerializer(athlete)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        athletes = Athlete.objects.all()
        serializer = AthleteSerializer(athletes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = AthleteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        athlete = get_object_or_404(Athlete, pk=pk)
        serializer = AthleteSerializer(athlete, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        athlete = get_object_or_404(Athlete, pk=pk)
        athlete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
