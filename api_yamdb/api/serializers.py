from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.constants import MAX_LENGTH_USERNAME, MAX_LENGTH_EMAIL
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_not_me
from .mixins import UserSerializerMixin


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=(UnicodeUsernameValidator(), validate_not_me),
    )
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL)

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

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(UnicodeUsernameValidator(),),
    )
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        attrs['user'] = user

        if not default_token_generator.check_token(
            user, attrs['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )

        return attrs


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
            'rating',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False,
        allow_null=False,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def to_representation(self, instance):
        """Возвращаем полные объекты для category и genre, а также rating."""
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, attrs):
        request = self.context.get('request')
        view = self.context.get('view')

        if self.instance is None and request and view:
            title_id = view.kwargs.get('title_id')
            review_exists = Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists()

            if review_exists:
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class UserSerializer(UserSerializerMixin):

    class Meta(UserSerializerMixin.Meta):
        read_only_fields = ('role',)


class AdminUserSerializer(UserSerializerMixin):
    pass
