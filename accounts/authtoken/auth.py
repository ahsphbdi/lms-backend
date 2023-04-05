try:
    from hmac import compare_digest
except ImportError:
    def compare_digest(a, b):
        return a == b

import binascii
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header,
)

from accounts.authtoken.crypto import hash_token
from accounts.authtoken.models import AuthToken
from accounts.authtoken.settings import CONSTANTS, knox_settings
from accounts.authtoken.signals import token_expired


class TokenAuthentication(BaseAuthentication):
    '''
    This authentication scheme uses Knox AuthTokens for authentication.

    Similar to DRF's TokenAuthentication, it overrides a large amount of that
    authentication scheme to cope with the fact that Tokens are not stored
    in plaintext in the database

    If successful
    - `request.user` will be a django `User` instance
    - `request.auth` will be an `AuthToken` instance
    '''


    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = knox_settings.AUTH_HEADER_PREFIX.encode()

        if not auth:
            return None
        if auth[0].lower() != prefix.lower():
            # Authorization header is possibly for another backend
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. '
                    'Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        user, auth_token = self.authenticate_credentials(auth[1])
        return (user, auth_token)

    def authenticate_credentials(self, token):
        '''
        Due to the random nature of hashing a value, this must inspect
        each auth_token individually to find the correct one.

        Tokens that have expired will be deleted and skipped
        '''
        msg = _('Invalid token.')
        token = token.decode("utf-8")
        for auth_token in AuthToken.objects.filter(
                token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]):
            if self.token_not_ok(auth_token):
                continue

            try:
                digest = hash_token(token)
            except (TypeError, binascii.Error):
                raise exceptions.AuthenticationFailed(msg)
            if compare_digest(digest, auth_token.digest):
                if knox_settings.AUTO_REFRESH and auth_token.expiry:
                    self.renew_token(auth_token)
                return self.validate_user(auth_token)
        raise exceptions.AuthenticationFailed(msg)

    def renew_token(self, auth_token):
        current_expiry = auth_token.expiry
        new_expiry = datetime.now() + knox_settings.TOKEN_TTL
        auth_token.expiry = new_expiry
        # Throttle refreshing of token to avoid db writes
        delta = (new_expiry - current_expiry).total_seconds()
        if delta > knox_settings.MIN_REFRESH_INTERVAL:
            auth_token.save(update_fields=('expiry',))
    
    def validate_user(self, auth_token):
        
        if not auth_token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))
        return (auth_token.user, auth_token)

    def authenticate_header(self, request):
        return knox_settings.AUTH_HEADER_PREFIX

    def token_not_ok(self, auth_token):
        
        # move this logic to LoginView. when user is loged in we will delete expired tokens, it's better for performance!
        # for other_token in auth_token.user.auth_token_set.all():
        #     if other_token.digest != auth_token.digest and other_token.expiry:
        #         if other_token.expiry < timezone.now() or (other_token.last_use + knox_settings.LAST_USE_TO_EXPIRY) < timezone.now():
        #             other_token.delete()
        #             username = other_token.user.get_username()
        #             token_expired.send(sender=self.__class__,
        #                                username=username, source="other_token")
        
        if auth_token.expiry < datetime.now() or (auth_token.last_use + knox_settings.LAST_USE_TO_EXPIRY) < datetime.now():
            username = auth_token.user.get_username()
            auth_token.delete()
            token_expired.send(sender=self.__class__,
                                username=username, source="auth_token")
            return True
    
        return False