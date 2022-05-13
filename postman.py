import json
from datetime import datetime

import jwt
import requests

from core.environment import env

TOKEN_FILE = './assets/token.txt'


def read_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def write_token(value):
    with open(TOKEN_FILE, 'w') as f:
        return f.write(value)


def gen_response(function):
    def wrapper(*args, **kwargs):
        val = function(*args, **kwargs)
        print(json.dumps({
            'method': val.request.method,
            'status': val.status_code,
            'url': val.url,
            'response': None if not val.text else val.json(),
        }, indent=4))

    return wrapper


def gen_header(credential: dict):
    token = read_token()
    try:
        decoded_data = jwt.decode(token, env.secret_key, algorithms=[env.algorithm])
        print(
            f"current time:\t\t{datetime.now()}\n"
            + f"expire at:\t\t{datetime.fromtimestamp(decoded_data['exp'])}\n"
        )
    except jwt.ExpiredSignatureError as e:  # type: ignore
        print(f"<<<<<<<<{e}>>>>>>>>")
        write_token(BaseAPI.login('/login', data=credential).json()['access_token'])
        token = read_token()
    return {"Authorization": 'Bearer ' + token}


class BaseAPI:
    BASE_URL = "http://127.0.0.1:8000/api/"

    @classmethod
    def login(cls,
              url: str,
              data: dict):
        return requests.post(cls.BASE_URL + url, data=data)

    @classmethod
    @gen_response
    def get(cls,
            url: str,
            headers: dict | None = None,
            params: dict | None = None):
        return requests.get(cls.BASE_URL + url, headers=headers, params=params)

    @classmethod
    @gen_response
    def post(cls,
             url: str,
             headers: dict | None = None,
             json_data: dict | None = None,
             data: dict | None = None):
        return requests.post(cls.BASE_URL + url, headers=headers, json=json_data, data=data)

    @classmethod
    @gen_response
    def delete(cls,
               url: str,
               headers: dict | None = None):
        return requests.delete(cls.BASE_URL + url, headers=headers)

    @classmethod
    @gen_response
    def put(cls, url: str, headers: dict | None = None, json_data: dict | None = None):
        return requests.put(cls.BASE_URL + url, json=json_data, headers=headers)


TOKEN_URL = 'token/'
TOKEN_REFRESH_URL = 'token/refresh/'
TOKEN_VERIFY_URL = 'token/verify/'
REGISTER_URL = 'register/'

USER_LIST_URL = 'users/'
USER_DETAILS_URL = 'users/%d/'

BOOK_LIST_URL = 'books/'
BOOK_DETAILS_URL = 'books/%d/'

CART_LIST_URL = 'carts/'
CART_DETAILS_URL = 'carts/%d/'


def main():
    try:
        pk = int(input("id: "))

        # Authentication
        user = {'email': 'user03', "password": 'hello'}
        BaseAPI.post(REGISTER_URL, json_data=user)
        credential = {'username': 'user', "password": 'hello'}
        BaseAPI.post(TOKEN_URL, data=credential)

        # User
        BaseAPI.get(USER_LIST_URL)
        BaseAPI.get(USER_DETAILS_URL % pk)

        # Product
        BaseAPI.get(BOOK_LIST_URL)
        BaseAPI.get(BOOK_DETAILS_URL % pk)

        BaseAPI.get(CART_LIST_URL)
        BaseAPI.get(CART_DETAILS_URL % pk)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
