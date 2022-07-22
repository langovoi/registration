import sys

import firebase_admin
import requests
from firebase_admin import credentials

cred = credentials.Certificate("captcha.json")
r = firebase_admin.initialize_app(cred)
print()


s = requests.Session()
s.auth = ('rest_user', 'qB5sOHkkADe6LVc9')
users = s.get('http://agent.visaby.com/rest/germany')
print(users.text)