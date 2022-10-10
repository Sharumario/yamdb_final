from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = (
    (USER, 'пользователь'),
    (ADMIN, 'админ'),
    (MODERATOR, 'модератор'),
)
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 8
CATEGORY_GENRE_NAME_LENGTH = 256
CATEGORY_GENRE_SLUG_LENGTH = 50


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        'почта', max_length=EMAIL_LENGTH, unique=True,
    )
    first_name = models.CharField(
        'имя', max_length=USERNAME_LENGTH, blank=True,
    )
    last_name = models.CharField(
        'фамилия', max_length=USERNAME_LENGTH, blank=True,
    )
    role = models.CharField(
        'пользовательская роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField('биография', blank=True,)
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        null=True,
        blank=True,
        default='XXXX',
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class CategoryGenreBase(models.Model):
    name = models.CharField(
        'Название', max_length=CATEGORY_GENRE_NAME_LENGTH
    )
    slug = models.SlugField(
        'Идентификатор', max_length=CATEGORY_GENRE_SLUG_LENGTH, unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        'Название произведения',
        db_index=True
    )
    year = models.IntegerField(
        'год',
        validators=(validate_year, )
    )
    description = models.TextField(
        'Описание произведения',
        help_text='Введите описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseReviewComment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Review(BaseReviewComment):
    score = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
        )
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_reviews',
            )
        ]


class Comment(BaseReviewComment):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
