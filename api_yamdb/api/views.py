from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .serializers import SignupSerializer, TokenSerializer

User = get_user_model()


class SignupAPIView(APIView):
    """Получает в POST-запросе параметры email, username и отправляет письмо с
    кодом подтверждения на указанный email"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
            },
        )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    """Получает в POST-запросе параметры username, confirmation_code и
    возвращает токен, если confirmation_code верный"""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'token': access}, status=status.HTTP_200_OK)
