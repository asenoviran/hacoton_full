from rest_framework import generics, permissions
from rest_framework.generics import CreateAPIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request 
from .models import OwnerRequest
from .serializers import OwnerRequestSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import ChangePasswordSerializer, RegistrationSerializer, ActivationSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.authentication import TokenAuthentication



class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Thanks for registration!'})
    

class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response({'message': 'Аккаунт успешно активирован!'})


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        Token.objects.get(user=request.user).delete()
        return Response({'message': 'Вы вышли из аккаунта!'})
    

User = get_user_model()

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = OwnerRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

