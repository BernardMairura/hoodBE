import jwt
from rest_framework import authentication,exceptions
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import User
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    #overide authication
    def authenticate(self,request):
        #get headers
        auth_data=authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix,token=auth_data.decoder('utf-8').split('')

        try:
            # payload=jwt.decode(token,settings.JWT_SECRETE_KEY)

            # user=User.objects.get(username=payload['username'])
            # return(user,token)

             payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256", )
             user = User.objects.get(email=payload['email'])
             return(user,token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid,login')

        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired,login')


        return super().authenticate(request)