from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from store.models import Customer, Cart, CartItem
from .constants import THIRTY_DAYS_IN_SECONDS, FIVE_MINS_IN_SECONDS, ONE_DAY_IN_SECONDS
from .serializers import MergeAnonymousCartSerializer, SignUpSerializer

# Create your views here.


class TokenObtainPairCookieView(TokenObtainPairView):
    """Create JWT with cookies

        This class extracts access and refresh token from response, and set them as httpOnly cookies.
        The access token expires in 5 mins while refresh cookie expires in 1 day by default, if keep_me_signed_in
        is checked, then set the refresh cookie max age to 30 days

    Returns:
        access: access token
        refresh: refresh token

    Permissions: [AllowAny]
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
        # Set cookie expire date
        response.set_cookie(key='access', value=access_token,
                            httponly=True, samesite='Lax', max_age=FIVE_MINS_IN_SECONDS)
        response.set_cookie(key='refresh', value=str(data.get('refresh')),
                            httponly=True, samesite='Lax', max_age=refresh_token_max_age)

        return response


class TokenRefreshCookieView(TokenRefreshView):
    """Refresh JWT with cookies

       This class refresh access token, and set it as httpOnly cookie

    Returns:
       access: access token
    Permissions: [AllowAny]

    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        data = response.data
        access_token = data.get('access')

        response.set_cookie(key='access', value=access_token,
                            httponly=True, samesite='Lax', max_age=FIVE_MINS_IN_SECONDS)
        return response


class mergeAnonymousCartView(APIView):
    """Merge anonymous shopping cart to customer shopping cart

    This class merges anonymous shopping cart to customer shopping cart to keep the customer shopping cart updated.

    Returns:
        cart id of customer shopping cart
    Permissions: [IsAuthenticated]
    """
    permission_classes = [IsAuthenticated]

    def _merge_cart_items(self, source_cart_id, target_cart) -> str:
        """Merge cart items

        This method merges cart items of source cart to target cart, then delete the source cart and related items

        Args:
            source_cart_id (uuid): id of source cart
            target_cart (Cart instance): target cart

        Returns:
            str: uuid of merged cart
        """
        target_cart_id = target_cart.pk
        source_cart = Cart.objects.get(id=source_cart_id)
        source_cart_items = CartItem.objects.filter(cart_id=source_cart_id)
        with atomic():
            for item in source_cart_items:
                if CartItem.objects.filter(product_id=item.product.pk, cart_id=target_cart_id).exists():
                    customer_cart_item = CartItem.objects.get(
                        product_id=item.product, cart_id=target_cart_id)
                    customer_cart_item.quantity += item.quantity
                    customer_cart_item.save()
                    item.delete()
                else:
                    item.cart = target_cart
                    item.save()
            source_cart.delete()
        return target_cart_id

    def post(self, request, *args, **kwargs):
        merge_serializer = MergeAnonymousCartSerializer(data=request.data)
        if not merge_serializer.is_valid():
            return Response(merge_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        anonymous_cart_id = merge_serializer.validated_data.get(
            'anonymous_cart_id')

        data_copy = request.data.copy()

        if request.user.is_authenticated:
            customer = Customer.objects.get(user_id=request.user.pk)
            if customer.cart is None:
                # if customer cart is null and anonymous_cart is null, create a new one and bind it to the customer
                if anonymous_cart_id is None:
                    cart = Cart.objects.create()
                    customer.cart = cart
                    customer.save()
                    data_copy['anonymous_cart_id'] = str(cart.id)
                # if customer cart is null and anonymous_cart is not null, bind the anonymous_cart to the customer
                else:
                    customer.cart = Cart.objects.get(id=anonymous_cart_id)
                    customer.save()
                    data_copy['anonymous_cart_id'] = str(anonymous_cart_id)
            else:
                # if customer cart is not null and anonymous_cart is null, return customer cart
                if anonymous_cart_id is None:
                    data_copy['anonymous_carid'] = str(customer.cart.id)
                # if customer cart is not null and anonymous_cart is not null:
                # 1. merge anonymous cart to customer cart
                # 2. delete the anonymous cart and items
                else:
                    merged_cart_id = self._merge_cart_items(
                        source_cart_id=anonymous_cart_id, target_cart=customer.cart)
                    data_copy['anonymous_cart_id'] = str(merged_cart_id)

        updated_serializer = MergeAnonymousCartSerializer(data=data_copy)

        if updated_serializer.is_valid():
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(updated_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        customer = get_object_or_404(Customer, user_id=user_id)
        cart_id = customer.cart.id if customer.cart else None
        return Response({'cart_id': cart_id, 'first_name': customer.first_name, 'is_logged_in': request.user.is_authenticated})


class LogOutView(APIView):
    """Log Out with cookies

    This class clears JWT cookies
    Permissions: [AllowAny]
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class SignUpViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class IsUsernameOccupied(APIView):
    permission_classes = [AllowAny]

    def _createUsernameMessage(self, is_available: bool, message: str):
        return Response({'is_available': is_available, 'message': message})

    def get(self, request, *args, **kwargs):
        query_username = request.query_params.get('username')
        if query_username is None:
            raise ValidationError('username is required')
        username = User.objects.filter(username__iexact=query_username)
        msg = 'Username is already taken.' if username.exists() else 'Username is available.'
        return self._createUsernameMessage(is_available=not username.exists(), message=msg)
