from django.shortcuts import render
from rest_framework import generics
from .serializer import LoginSerializer,RegistrationSerializer
from rest_framework import status 
from rest_framework.response  import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib import auth
import jwt


# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer
    def post(self, request):
        """
        Handle user Signup
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.validate_password_(user)
        serializer.save()
        data = serializer.data
        return_message = {'message':"Signup Successful",
                          'user': data}
        return Response(return_message, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        user_name = data.get('user_name', '')
        password = data.get('password', '')
        user = auth.authenticate(username=user_name, password=password)

        if user:
            auth_token = jwt.encode(
                {'user_name': user.username}, settings.SECRET_KEY)

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




 
