from django.urls import path
from djangoapp.views.auth import registerView, loginView
from djangoapp.views.test import testTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenBlacklistView
)

urlpatterns = [
    path('test_token/', testTokenView.test, name='test_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('register/', registerView.register),
    path('login/', loginView.login),

]