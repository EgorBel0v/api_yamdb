from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentViewSet
from .views import (
    SignupView, GetTokenView, UsersViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet
)
app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
]
