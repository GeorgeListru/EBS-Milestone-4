from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserView, EmailTokenObtainPairView,UsersListView

urlpatterns = [
    path('users', UsersListView.as_view(), name='register_user'),
    path("register", RegisterUserView.as_view(), name="token_register"),
    path("token", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
