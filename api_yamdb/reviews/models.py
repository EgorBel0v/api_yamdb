from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import ValidationUsername

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """"Основная модель Юзеров."""
    """"Декоратор @property более удобный для работы, чтобы не дублировтаь код."""

    username = models.CharField(
        validators=(ValidationUsername,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Класс категорий(типов) произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс жанров произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
    )
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательный класс для жанров и произведений."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            )
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Класс отзывов для произведений."""

    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Отзыв'
    )
    score = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        ordering = ['pub_date']

    def __str__(self):
        return f'Отзыв {self.author} для {self.title}'


class Comments(models.Model):
    """Класс комментариев для отзывов."""
 
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Комментарий'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review}'
