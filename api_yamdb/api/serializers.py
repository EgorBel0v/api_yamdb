from rest_framework import serializers
from reviews.models import User, Genre, Category, Title, Comments, Review
import datetime as dt


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializerGET(serializers.ModelSerializer):
    """Сериализатор для модели Title для GET-запросов."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class TitleSerializerOTHER(serializers.ModelSerializer):
    """Сериализатор для модели Title для других запросов."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

        def validate_year(self, value):
            year = dt.date.today().year
            if year > value:
                raise serializers.ValidationError(
                    'Произведение еще не вышло! Проверьте год'
                )
            return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Можно оставить только 1 отзыв')
        return data

    class Meta:
        exclude = ('title',)
        read_only_fields = (
            'id',
            'pub_date',
            'author'
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ('review',)
        read_only_fields = (
            'id',
            'pub_date',
            'author'
        )
        model = Comments
