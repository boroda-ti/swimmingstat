from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .permissions import IsOwnerOrStaff
from .serializers import CustomUserSerializer

class LoginAPIView(APIView):

    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        is_coach = CustomUser.objects.get(email=request.data['email']).is_coach

        if not is_coach:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(email=request.data['email'], password=request.data['password'])
        serializer = CustomUserSerializer(user)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserDetailUpdateAPIView(RetrieveUpdateAPIView):
    
    permission_classes = [IsOwnerOrStaff]
    serializer_class = CustomUserSerializer

    def get_object(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return user