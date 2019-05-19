import json

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from google_auth_oauthlib.flow import Flow
from rest_framework.reverse import reverse

from .views import Oauth2Callback


class GoogleOauth2Callback(Oauth2Callback):
    def get(self, request, *args, **kwargs):
        client_secrets = json.loads(settings.GOOGLE_CLIENT_SECRETS)
        flow = Flow.from_client_config(
            client_secrets,
            scopes=['profile', 'email'],
            redirect_uri=reverse('user:google_oauth2callback', request=self.request))

        if 'code' not in self.request.GET:
            url, state = flow.authorization_url()
            return HttpResponseRedirect(url)
        else:
            auth_code = self.request.GET['code']
            token = flow.fetch_token(code=auth_code)
            user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo',
                                     params={'access_token': token.access_token}).json()
            username = f"google-{user_info['sub']}"
            email = user_info['email'] or ''

            ott = self.save_user(username, email, user_info)
            context = {
                'ott': ott,
                'redirect_url': '/stations/list'
            }
            return self.render_to_response(context)
