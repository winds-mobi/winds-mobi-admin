import json

from django.conf import settings
from django.http import HttpResponseRedirect
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from .views import Oauth2Callback


class FacebookOauth2Callback(Oauth2Callback):
    graph_api_version = 'v2.12'

    authorization_base_url = 'https://www.facebook.com/dialog/oauth?scope=public_profile&scope=email'
    token_url = f'https://graph.facebook.com/{graph_api_version}/oauth/access_token'
    me_url = f'https://graph.facebook.com/{graph_api_version}/me?fields=id,name,first_name,last_name,gender,email,link,\
    birthday,age_range,timezone,website,location,locale,devices'

    def get(self, request, *args, **kwargs):
        facebook = OAuth2Session(settings.FACEBOOK_CLIENT_ID, redirect_uri=settings.FACEBOOK_REDIRECT_URI)
        facebook = facebook_compliance_fix(facebook)

        if 'code' not in self.request.GET:
            authorization_url, state = facebook.authorization_url(self.authorization_base_url)
            return HttpResponseRedirect(authorization_url)
        else:
            auth_code = self.request.GET['code']
            facebook.fetch_token(self.token_url, client_secret=settings.FACEBOOK_CLIENT_SECRET, code=auth_code)
            user_info = json.loads(facebook.get(self.me_url).text)
            username = f"facebook-{user_info['id']}"
            email = user_info['email'] or ''

            ott = self.save_user(username, email, user_info)
            context = {
                'ott': ott,
                'redirect_url': '/stations/list'
            }
            return self.render_to_response(context)
