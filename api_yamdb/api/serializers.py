from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(UnicodeUsernameValidator(),),
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.'
            )

        return value

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError(
                {'username': 'Такой username уже используется.'}
            )

        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError(
                {'email': 'Такой email уже используется.'}
            )

        return attrs
