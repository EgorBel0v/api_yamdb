from rest_framework import serializers
from reviews.models import User, Category, Genre, Title, Comments, Review


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
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerGET(serializers.ModelSerializer):
    """Сериализатор для модели Title для GET-запросов."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Reviews."""

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
    """Сериалайзер для модели Comments."""

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
