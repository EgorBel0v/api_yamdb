from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins

from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializerGET, TitleSerializerOTHER
)

from reviews.models import Category, Genre, Title

from .permissions import ReadOnlyPermission, IsAdminPermission


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
    permission_classes = (ReadOnlyPermission, IsAdminPermission)


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
    permission_classes = (ReadOnlyPermission, IsAdminPermission)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializerOTHER
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = (ReadOnlyPermission, IsAdminPermission)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializerOTHER
