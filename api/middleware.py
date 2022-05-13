import logging
from threading import local

from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger()
_user_id = local()


class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(self, request, exception):
        logger.exception(exception)

    def process_template_response(self, request, response):
        if hasattr(response, 'data'):
            print(response.status_text)
            response.data = {
                'msg': response.status_text,
                'status_code': response.status_code,
                'data': response.data,
            }
        return response

    def __call__(self, request):
        try:
            if not request.headers.get('Authorization'):
                raise Exception(f"{request.path}:\tUnauthorized Access")
            _, token = request.headers.get('Authorization', " ").split(' ')
            auth = JWTAuthentication()
            _user_id.val = auth.get_user(auth.get_validated_token(token)).id
        except Exception as e:
            print("middleware>>", e)
        return self.get_response(request)


def get_current_user():
    return _user_id.val
