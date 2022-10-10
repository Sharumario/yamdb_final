from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title, User,
    EMAIL_LENGTH, USERNAME_LENGTH, CONFIRMATION_CODE_LENGTH
)
from reviews.validators import (
    validate_username, validate_year
)


class UserSerializer(serializers.ModelSerializer):

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
        return validate_username(value)


class UserAuthSerializers(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH, required=True,
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH, required=True,
    )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = ('__all__',)
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    def validate_year(self, value):
        return validate_year(value)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        if (
            self.context['view'].action not in ('update', 'partial_update')
            and Review.objects.filter(
                author=self.context['request'].user,
                title=get_object_or_404(
                Title, pk=self.context['view'].kwargs.get('title_id')
                )).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв!')
        return attrs

    class Meta:
        model = Review
        exclude = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
