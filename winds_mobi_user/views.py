import binascii
import os
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.views.generic import TemplateView
from redis.client import Redis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from winds_mobi_admin.authentication import IsJWTAuthenticated, JWTAuthentication
from winds_mobi_user.models import Profile, SocialAuth

User = get_user_model()


def get_ott_key(ott):
    return f"login-ott/{ott}"


class LoginView(APIView):
    """
    Login into API with a One Time Token or a Django username/password
    Return a JWT token
    """

    # Don't use any django default authentication here
    authentication_classes = ()

    def post(self, request):
        ott = request.data.get("ott")
        username = request.data.get("username")
        password = request.data.get("password")

        if ott:
            username = redis.getdel(get_ott_key(ott))
            if not username:
                return Response(
                    {"code": -11, "detail": "Unable to find One Time Token"}, status=status.HTTP_401_UNAUTHORIZED
                )
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"code": -12, "detail": "Unable to get user"}, status=status.HTTP_401_UNAUTHORIZED)
            token = jwt.encode(
                {"username": username, "exp": datetime.utcnow() + timedelta(days=30)},
                key=settings.SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM,
            )
            return Response({"token": token})
        elif username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token = jwt.encode(
                        {"username": username, "exp": datetime.utcnow() + timedelta(days=30)},
                        key=settings.SECRET_KEY,
                        algorithm=settings.JWT_ALGORITHM,
                    )
                    return Response({"token": token})
                else:
                    return Response(
                        {"code": -22, "detail": "The password is valid, but the account has been disabled"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(
                    {"code": -21, "detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response({"code": -1, "detail": "Bad parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Get the profile of authenticated user
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsJWTAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user)

        profile = Profile.objects.filter(user=user).first()
        profile_data = {}
        if profile:
            profile_data.update(profile.data)

        social_auth = SocialAuth.objects.filter(user=user).first()
        if social_auth:
            if social_auth.provider == "facebook":
                profile_data["picture"] = f"https://graph.facebook.com/{social_auth.provider_id}/picture"
                profile_data["display-name"] = social_auth.data.get("first_name")
            elif social_auth.provider == "google":
                profile_data["picture"] = social_auth.data.get("picture")
                profile_data["display-name"] = social_auth.data.get("given_name")
            else:
                profile_data["display-name"] = user.username

        # Compatibility with winds-mobi-js-client
        profile_data["_id"] = user.username
        if social_auth:
            profile_data["user-info"] = social_auth.data

        return Response(profile_data)

    def delete(self, request):
        user = User.objects.get(username=request.user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileFavoriteView(APIView):
    """
    Manage favorites stations list
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsJWTAuthenticated,)

    def post(self, request, station_id):
        user = User.objects.get(username=request.user)
        with transaction.atomic():
            profile, created = Profile.objects.select_for_update().get_or_create(user=user)
            favorites = profile.data.setdefault("favorites", [])
            if station_id not in favorites:
                favorites.append(station_id)
                profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, station_id):
        user = User.objects.get(username=request.user)
        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(user=user)
            if profile and "favorites" in profile.data:
                favorites = profile.data["favorites"]
                if station_id in favorites:
                    favorites.remove(station_id)
                    profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Oauth2Callback(TemplateView):
    template_name = "winds_mobi_user/oauth2_callback.html"

    def authenticate(self):
        pass

    def save_user_auth(self, provider, provider_id, email, user_info):
        username = f"{provider}-{provider_id}"  # For now, we create a django account for each social auth
        try:
            social_auth = SocialAuth.objects.get(provider=provider, provider_id=provider_id)
            user = social_auth.user
            user.email = email
            user.data = user_info
            # Update last_login field when a user does a social login (jwt token expired, ...)
            user.last_login = datetime.now(timezone.utc)
            user.save()
        except SocialAuth.DoesNotExist:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email})
            SocialAuth.objects.create(provider=provider, provider_id=provider_id, user=user, data=user_info)

        # Generate One Time Token for API authentication
        ott = binascii.hexlify(os.urandom(20)).decode("ascii")
        redis.set(get_ott_key(ott), username, ex=30)
        return ott


redis = Redis.from_url(url=settings.REDIS_URL, decode_responses=True)
