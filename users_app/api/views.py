from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer
from users_app import models


class RegistrationAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()

            data['response'] = "Successfully registered new user."
            data['username'] = user.username
            data['email'] = user.email

            # token, created = Token.objects.get_or_create(user=user)
            # data['token'] = token.key

            refresh = RefreshToken.for_user(user)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST', ])
# def logout_view(request):
#
#     if request.method == 'POST':
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)