from rest_framework import serializers 
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    # Ensure email is provided and is unique
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exist",
            )
        ],
        error_messages={
            'required': "Email is a required field",
        }
    )
 
    # characters, and can not be read by the client.
    password = serializers.CharField(
            required=True,
            allow_null=False,
            write_only=True,
            min_length=6,
    )
    confirm_password = serializers.CharField(
            write_only=True,
            required=True,
            allow_null=False,
            min_length=6,)
    user_name = serializers.CharField(
            required=True,
            allow_null=False,
            min_length=2,
            validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username already exist",
            )
        ],
        error_messages={
            'required': "Username is a required field",
        }
    )
    # controls how a client handles a token when doing registration
    
    token = serializers.CharField(read_only=True)

    @staticmethod
    def validate_password_(data):
        password = data.get('password', None)
        confirm_password = data.get('password', None)
        # Raises an exception where username and password is not provided.
       
        if confirm_password != password:
            raise serializers.ValidationError(
                'Confirmed Password and Password should match .'
            )
        return data 

    class Meta:
        model = User
        
        fields = ['user_name', 'email',
                  'password','confirm_password','is_superuser','is_admin','is_occupant',  'token']


    @classmethod
    def create(self, data):
        del data["confirm_password"]
        
        return User.objects.create_user(**data)

class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""
    user_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    @staticmethod
    def validate(data):
        user_name = data.get('user_name', None)
        password = data.get('password', None)
   
        if user_name is None:
            raise serializers.ValidationError(
                'An user_name is required to log in.'
            )
    
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = authenticate(user_name=user_name, password=password)
        
        # Raise an exception in this case if no user is returned.

        if user is None:
            raise serializers.ValidationError(
                'A user with this user_name and password was not found.'
            )
       #returns dictionary of data validated
        return {
            'user_name': user.user_name,
            'email':user.email,
            'token': user.token,
        }

    