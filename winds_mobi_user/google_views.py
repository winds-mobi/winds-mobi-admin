import json

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from google_auth_oauthlib.flow import Flow
from rest_framework.reverse import reverse

from winds_mobi_user.views import Oauth2Callback


class GoogleOauth2Callback(Oauth2Callback):
    def get(self, request, *args, **kwargs):
        with open(settings.GOOGLE_CLIENT_SECRET) as config_file:
            client_secret = json.load(config_file)
            flow = Flow.from_client_config(
                client_secret,
                scopes=['openid',
                        'https://www.googleapis.com/auth/userinfo.profile',
                        'https://www.googleapis.com/auth/userinfo.email'],
                redirect_uri=reverse('user:google_oauth2callback', request=self.request))

            if 'code' not in self.request.GET:
                url, state = flow.authorization_url()
                return HttpResponseRedirect(url)
            else:
                auth_code = self.request.GET['code']
                token = flow.fetch_token(code=auth_code)
                user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo',
                                         params={'access_token': token['access_token']}).json()
                ott = self.save_user_auth('google', user_info['sub'], user_info['email'], user_info)
                context = {
                    'ott': ott,
                    'redirect_url': '/stations/list'
                }
                return self.render_to_response(context)
