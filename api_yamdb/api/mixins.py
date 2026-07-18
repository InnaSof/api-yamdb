from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializerMixin(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.'
            )
        return value
