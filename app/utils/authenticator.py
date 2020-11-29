import os
from base64 import b64encode

def checkAuthenticator(auth):
  auth_username = os.getenv('API_HEADERS_USERNAME')
  auth_password = os.getenv('API_HEADERS_PASSWORD')
  b64E = b64encode((auth_username + ':' + auth_password).encode('ascii')).decode('ascii')
  true_auth = 'Basic ' + b64E
  return auth == true_auth