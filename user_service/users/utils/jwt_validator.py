import requests
import json
from jose import jwt
from jose.exceptions import JWTError
from cachetools import TTLCache

AUTH0_DOMAIN = 'YOUR_DOMAIN.auth0.com'
API_AUDIENCE = 'YOUR_API_IDENTIFIER'
ALGORITHMS = ['RS256']
JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

# Cache JWKS for 10 minutes
_jwks_cache = TTLCache(maxsize=1, ttl=600)


def get_jwks():
    if 'jwks' not in _jwks_cache:
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        _jwks_cache['jwks'] = response.json()
    return _jwks_cache['jwks']


def get_rsa_key(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            return {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    raise JWTError("Public key not found.")


def verify_token(token):
    rsa_key = get_rsa_key(token)
    return jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer=f'https://{AUTH0_DOMAIN}/'
    )
