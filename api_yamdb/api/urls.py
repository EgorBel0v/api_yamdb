from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GetTokenView, SignupView, UsersViewSet

app_name = 'api'

router = SimpleRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
]