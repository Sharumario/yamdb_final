import random

from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (
    IsAdmin, IsAdminUserOrReadOnly, IsAuthorModerAdminOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer,
    ReviewsSerializer, TitleReadSerializer,
    TitlesSerializer, TitleWriteSerializer, TokenSerializer,
    UserAuthSerializers, UserSerializer
)
from api.filters import TitleFilter
from reviews.models import (
    Category, Genre, Review, Title, User,
    CONFIRMATION_CODE_LENGTH
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', )

    @action(methods=['get', 'patch'],
            detail=False,
            serializer_class=UserSerializer,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            return Response(
                self.get_serializer(user).data,
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserAuthSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response(
            'Такой username или email уже существует',
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = ''.join(
        random.sample('0123456789', CONFIRMATION_CODE_LENGTH)
    )
    user.save()
    email = EmailMessage(
        subject='Код подтвержения для доступа к API!',
        body=f'Здравствуйте, {username}. '
             f'\nКод подтвержения для доступа к API:{user.confirmation_code}',
        to=[email]
    )
    email.send(fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


def clear_code(user):
    user.confirmation_code = ''
    user.save()


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if (
        user.confirmation_code == serializer.data['confirmation_code']
        and user.confirmation_code != ''
    ):
        token = AccessToken.for_user(user)
        clear_code(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    clear_code(user)
    return Response((
        'Либо вы ошиблись, либо вы хотите обновить код подтверждения. '
        'Введите username и email через api/v1/auth/signup/. '
        'Получите код и попытайтесь снова получить токен. '
        'Все эти заморочки во благо безопасности ваших данных! '
        'Благодарим за понимание!'
    ),
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryGenreBaseViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('-rating', 'category', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review())
