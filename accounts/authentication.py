import requests
import logging
from django.contrib.auth import get_user_model
from django.conf import settings
# import sys
PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
User = get_user_model()


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        logging.warning('entering authenticate function')
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': settings.DOMAIN},
        )
        logging.warning('got response for persona.')
        logging.warning(response.content.decode())
        if response.ok and response.json().get('status') == 'okay':
            email = response.json().get('email')
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None