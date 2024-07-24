from django.urls import path, include
from .views import CheckUserStatusView, TokenObtainPairCookieView, TokenRefreshCookieView, LogOutView, mergeAnonymousCartView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('check-user-status/', CheckUserStatusView.as_view(),
         name='check_user_status'),
    path('merge-cart/', mergeAnonymousCartView.as_view(),
         name='merge_anonymous_cart'),
    path('login/', TokenObtainPairCookieView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshCookieView.as_view(), name='refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
