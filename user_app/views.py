from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate

class LoginAPIView(APIView):

    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = authenticate(email=request.data['email'], password=request.data['password'])

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)