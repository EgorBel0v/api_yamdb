from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import permissions, status, viewsets, filters, mixins
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AdminModeratorAuthor
from reviews.models import Title, Review
from django.core.mail import EmailMessage
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from reviews.models import User, Category, Genre, Title, Review

from .permissions import AdminOnly, ReadOnly, AdminModeratorAuthor
from .filters import TitleFilter

from .serializers import (
    GetTokenSerializer, NotAdminSerializer,
    SignUpSerializer, UsersSerializer,
    CategorySerializer, GenreSerializer,
    TitleSerializerGET, TitleSerializerOTHER,
    ReviewSerializer, CommentSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['post', 'get', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class GetTokenView(APIView):
    """Получение JWT-токена. Права доступа - Доступно без токена."""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    """Получение подтверждения на переданный email. Доступно без токена."""

    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        data = {
            'email_body': (
                f'Приветствуем, {username}.'
                f'\nВаш личный код подтверждения для доступа к API: {{confirmation_code}}'
            ),
            'to_email': email,
            'email_subject': 'Код подтверждения для доступа к API!'
        }

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            if user.email != email:
                return Response({'error': 'Email не соответствует зарегистрированному пользователю.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SignUpSerializer(user, data=request.data)
        else:
            serializer = SignUpSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data['email_body'] = data['email_body'].format(confirmation_code=user.confirmation_code)
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)





class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (ReadOnly | AdminOnly,)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (ReadOnly | AdminOnly,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializerOTHER
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (ReadOnly | AdminOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializerOTHER


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        AdminModeratorAuthor,
        permissions.IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        queryset = title.reviews.order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comments."""

    permission_classes = (
        AdminModeratorAuthor,
        permissions.IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
