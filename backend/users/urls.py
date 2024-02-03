from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import UserViewSet, CurrentUserView, RegisterUser, LogoutView  # , ChangePasswordView

router = routers.SimpleRouter()
router.register(r'', UserViewSet)
# router.register(r'', CurrentUserView, basename='curr')
# router.register(r'profile/', UserProfileView)


## test ##
urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('login-refresh', TokenRefreshView.as_view()),
    path('signup', RegisterUser.as_view()),
    path('', include(router.urls)),
    path('current/', CurrentUserView.as_view(), name='current-user'),
    path('logout', LogoutView.as_view(), name='logout')

    # ========================#
    # Create change password
    # ========================#
    
    #path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # path('login', CustomAuthToken.as_view()),
]