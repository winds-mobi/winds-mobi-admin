import binascii
import os
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import TemplateView
from pymongo import ASCENDING
from pymongo import MongoClient, uri_parser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from winds_mobi_admin.authentication import JWTAuthentication, IsJWTAuthenticated


class Login(APIView):
    """
    Login into API with a One Time Token or a Django username/password
    Return a JWT token
    """

    # Don't use any django default authentication here
    authentication_classes = ()

    def post(self, request):
        ott = request.data.get('ott')
        username = request.data.get('username')
        password = request.data.get('password')

        if ott:
            ott_doc = mongo_db.login_ott.find_one_and_delete({'_id': ott})
            if not ott_doc:
                return Response({
                    'code': -11,
                    'detail': 'Unable to find One Time Token'},
                    status=status.HTTP_401_UNAUTHORIZED)
            username = ott_doc['username']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({
                    'code': -12,
                    'detail': 'Unable to get user'},
                    status=status.HTTP_401_UNAUTHORIZED)
            token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(days=30)},
                               key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            return Response({'token': token})
        elif username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(days=30)},
                                       key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
                    return Response({'token': token})
                else:
                    return Response({
                        'code': -22,
                        'detail': 'The password is valid, but the account has been disabled'},
                        status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'code': -21,
                    'detail': 'Invalid username or password'},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'code': -1,
                'detail': 'Bad parameters'},
                status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    """
    Get the profile of authenticated user
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsJWTAuthenticated,)

    def get(self, request):
        profile = mongo_db.users.find_one(request.user)
        if profile:
            return Response(profile)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProfileFavorite(APIView):
    """
    Manage favorites stations list
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsJWTAuthenticated,)

    def post(self, request, station_id):
        mongo_db.users.update_one({'_id': request.user},
                                  {'$addToSet': {'favorites': station_id}},
                                  upsert=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, station_id):
        mongo_db.users.update_one({'_id': request.user},
                                  {'$pull': {'favorites': station_id}},
                                  upsert=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Oauth2Callback(TemplateView):
    template_name = 'winds_mobi_user/oauth2_callback.html'

    def authenticate(self):
        pass

    def save_user(self, username, email, user_info):
        # Save user in Django
        try:
            user = User.objects.get(username=username)
            user.email = email
            # Update last_login field when a user does a social login (jwt token expired, ...)
            user.last_login = timezone.now()
        except User.DoesNotExist:
            user = User(username=username, email=email)
        user.save()

        # Save user_info
        mongo_db.users.update_one({'_id': username}, {'$set': {'user-info': user_info}}, upsert=True)

        # Generate One Time Token for API authentication
        mongo_db.login_ott.create_index([('createdAt', ASCENDING)], expireAfterSeconds=30)
        ott = binascii.hexlify(os.urandom(20)).decode('ascii')
        mongo_db.login_ott.insert_one({'_id': ott, 'username': username, 'createdAt': datetime.utcnow()})

        return ott


uri = uri_parser.parse_uri(settings.MONGODB_URL)
mongo_client = MongoClient(uri['nodelist'][0][0], uri['nodelist'][0][1])
mongo_db = mongo_client[uri['database']]
