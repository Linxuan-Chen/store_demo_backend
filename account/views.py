from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from store.models import Customer
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import timedelta
from .constants import THIRTY_DAYS_IN_SECONDS, FIVE_MINS_IN_SECONDS, ONE_DAY_IN_SECONDS
from rest_framework import status
from utils.createApiResponseMessage import createApiResponseMessage

# Create your views here.


class TokenObtainPairCookieView(TokenObtainPairView):
    """Create JWT with cookies

        This class extracts access and refresh token from response, and set them as httpOnly cookies.
        The access token expires in 5 mins while refresh cookie expires in 1 day by default, if keep_me_signed_in
        is checked, then set the refresh cookie max age to 30 days

    Returns:
        access: access token
        refresh: refresh token

    Permissions: [any]
    """
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        data = response.data
        access_token = data.get('access')
        refresh_token = data.get('refresh')
        keep_me_signed_in = data.get('keep_me_signed_in')
        refresh_token_max_age = ONE_DAY_IN_SECONDS
        if keep_me_signed_in:
            new_refresh_token = RefreshToken(refresh_token)
            new_refresh_token.set_exp(lifetime=(timedelta(days=30)))
            data['refresh'] = str(new_refresh_token)
            refresh_token_max_age = THIRTY_DAYS_IN_SECONDS
        print(access_token)
        # Set cookie expire date
        response.set_cookie(key='access', value=access_token,
                            httponly=True, samesite='Strict', max_age=FIVE_MINS_IN_SECONDS)
        response.set_cookie(key='refresh', value=str(data.get('refresh')),
                            httponly=True, samesite='Strict', max_age=refresh_token_max_age)

        return response


class TokenRefreshCookieView(TokenRefreshView):
    """Refresh JWT with cookies

       This class refresh access token, and set it as httpOnly cookie

    Returns: 
       access: access token
    Permissions: [any]

    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        data = response.data
        access_token = data.get('access')

        response.set_cookie(key='access', value=access_token,
                            httponly=True, samesite='Strict', max_age=FIVE_MINS_IN_SECONDS)
        return response


class CheckUserStatusView(APIView):
    """Check User Status

        This class checks if user is signed in.

    Returns:
        cart_id: shopping cart id of current user
        first_name: first name of customer

    Permissions: [Any]
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id  # type: ignore
        customer = Customer.objects.get(user_id=user_id)
        return Response({'cart_id': customer.cart, 'first_name': customer.first_name})


class LogOutView(APIView):
    """Log Out with cookies


    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg = createApiResponseMessage('User successfully logged out')
        response = Response(msg, status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response