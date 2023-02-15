from django.urls import path, include

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

from rest_framework.routers import DefaultRouter

V1_router = DefaultRouter()

V1_router.register('categories', CategoryViewSet)
V1_router.register('genres', GenreViewSet)
V1_router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(V1_router.urls)),
]