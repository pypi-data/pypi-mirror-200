from abc import ABC
from typing import Optional

from dnastack import ServiceEndpoint
from dnastack.client.base_client import BaseServiceClient
from dnastack.http.authenticators.factory import HttpAuthenticatorFactory
from dnastack.http.authenticators.oauth2 import OAuth2Authenticator


class NamespaceError(RuntimeError):
    """ Raised when the access to the API requires an authentication. """

    def __init__(self, message: str):
        super(NamespaceError, self).__init__(f'Namespace error: {message}')


class BaseWorkbenchClient(BaseServiceClient, ABC):
    def __init__(self, endpoint: ServiceEndpoint, namespace: Optional[str] = None):
        super().__init__(endpoint)
        if namespace:
            self.__namespace = namespace
        else:
            self.__namespace = self.__extract_namespace_from_auth(endpoint)

        self._logger.debug(f"Authenticated workbench services for namespace {self.__namespace}")

    @property
    def namespace(self):
        return self.__namespace

    @classmethod
    def __extract_namespace_from_auth(cls, endpoint: ServiceEndpoint) -> str:
        for authenticator in HttpAuthenticatorFactory.create_multiple_from(endpoint=endpoint):
            if isinstance(authenticator, OAuth2Authenticator):
                session_info = authenticator.initialize()
                return session_info.access_token_claims().sub
        raise NamespaceError("Could not extract namespace from request and no value was provided")
