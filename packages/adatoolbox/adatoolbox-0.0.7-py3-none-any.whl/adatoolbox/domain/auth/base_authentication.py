import requests
from loguru import logger
from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _
from requests.exceptions import ConnectionError, HTTPError, Timeout

from adatoolbox.domain.auth.settings import API_AD_URL
# from core.exceptions.gateway_timeout import GatewayTimeout

 
class AuthApiAuthentication(authentication.BaseAuthentication):
    """Auth Api Authentication Class."""

    def authenticate(self, request) -> tuple:
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise exceptions.AuthenticationFailed(_("Authorization header not found"))

        try:
            headers = {"Authorization": f"{token} "}
            url = f"{API_AD_URL}/api-ad/api/usuarios/userdata/"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json(), token
        except HTTPError as error:
            logger.debug(f"JWT Token {token[:3]}**** is Invalid. Permission Denied.")
            raise exceptions.PermissionDenied(_("Not authorized")) from error
        except (ConnectionError, Timeout) as error:
            # sentry_sdk.capture_exception(error)
            # raise GatewayTimeout(_("Request timeout for Auth-Api server")) from error
            pass