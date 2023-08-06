class PythonAnywhereAPIException(Exception):
    """ Base server side exception """


class InvalidTokenError(PythonAnywhereAPIException):
    """ Invalid API token (status code 401) """


class PermissionDeniedError(PythonAnywhereAPIException):
    """ Wrong username or somthing else (status code 403) """


class NotFoundError(PythonAnywhereAPIException):
    """ Path not found (status code 404) """


class StatusError(PythonAnywhereAPIException):
    """ Status code >= 400 (except 401, 403, 404) """


class PawapiException(Exception):
    """ Base client side exception """


class InvalidJSONError(PawapiException):
    """ Error while parsing json response """


class InvalidCredentialsError(PawapiException):
    """ Username or Token has an invalid character """


class RequestTimeoutError(PawapiException):
    """ Request timed out """
