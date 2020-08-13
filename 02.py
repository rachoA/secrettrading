import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'vrsFMkxrMkXgOL6cThSkYRP4QgwRDvSxBF3zSY11'
secret_key = 'dE5RzA8Nx9ixkUbdY9vNVMJ4EkMG5BLQvhZ4aB8H'
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

print(headers)

res = requests.get(server_url + "/v1/accounts", headers=headers)

print(res.json())
