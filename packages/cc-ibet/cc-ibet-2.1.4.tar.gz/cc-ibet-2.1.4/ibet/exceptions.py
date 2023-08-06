from api_helper.exceptions import *


class FrequentlyRequestException(Exception):
    pass


class AuthenticationError(BaseAuthenticationError):
    pass
