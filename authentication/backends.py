import jwt
from rest_framework import authentication,exceptions
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import User
from .models import User


# class JWTAuthentication(authentication.BaseAuthentication):
#     #overide authication
#     def authenticate(self,request):
#         #get headers
#         auth_data=authentication.get_authorization_header(request)

#         if not auth_data:
#             return None

#         prefix,token=auth_data.decoder('utf-8').split('')

#         try:
#             # payload=jwt.decode(token,settings.JWT_SECRETE_KEY)

#             # user=User.objects.get(username=payload['username'])
#             # return(user,token)

#              payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256", )
#              user = User.objects.get(email=payload['email'])
#              return(user,token)

#         except jwt.DecodeError as identifier:
#             raise exceptions.AuthenticationFailed('Your token is invalid,login')

#         except jwt.ExpiredSignatureError as identifier:
#             raise exceptions.AuthenticationFailed('Your token is expired,login')


#         return super().authenticate(request)



def get_token_data(token):
    """
    checks validity of a token
    Args:
        token (str): token to be validated
    Return:
        user (obj): valid user object
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256", )
        user = User.objects.get(email=payload['email'])
    except Exception as error:
        exception_mapper = {
            jwt.ExpiredSignatureError: "Token expired. Please login to get a new token.",
            jwt.DecodeError: "Authorization failed due to an Invalid token.",
        }
        message = exception_mapper.get(
            type(error), 'Authorization failed.')
        raise exceptions.AuthenticationFailed(message)
    return user
class JWTAuthentication(authentication.BaseAuthentication):
    """
    This is called on every request to check if the user is authenticated
    """
    @classmethod
    def authenticate(self, request):
        """
        This checks that the passed JWT token is valid and returns
        a user and his/her token on successful verification
        """
        # Get the passed token
        auth_header = authentication.get_authorization_header(
            request).decode('utf-8')
        if not auth_header or auth_header.split()[0].lower() != 'bearer':
            return None
        token = auth_header.split(" ")[1]
        # Attempt decoding the token
        user = get_token_data(token)
        return (user, token)
