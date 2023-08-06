from os import environ
import logging


class MissingEnvVariablesError(Exception):
    pass


# The URL for the 42 API token endpoint.
token_url: str = 'https://api.intra.42.fr/oauth/token'

# The base URL for a 42 API request.
api_url: str = 'https://api.intra.42.fr/v2/'

env_variables: list = ["UID42", "SECRET42", "SCOPE"]

if not all(map(lambda var: var in environ, env_variables)):
    raise MissingEnvVariablesError(
        "Missing environment variables. Make sure .env was sourced.")

# Environment variables
# The 42 client ID, used to authenticate with the 42 API.
UID_42 = environ['UID42']
# The 42 client secret, used to authenticate with the 42 API.
SECRET_42 = environ['SECRET42']
# The scope of the 42 API access token.
SCOPE = environ['SCOPE']

# Request parameters
# These parameters are used when requesting an access token from the 42 API.
# Grant type specifies the type of grant being requested (in this case, a
# client credential grant).
params: dict = {
    'grant_type': 'client_credentials',
    'client_id': UID_42,
    'client_secret': SECRET_42,
    'scope': SCOPE,
}

# Dictionary mapping string values for log levels to the corresponding integer
# values used by the logging module.
log_lvls = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'FATAL': logging.FATAL
}
