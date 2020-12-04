from rest_framework import serializers 
from .models import User 
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
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['user_name', 'email',
                  'password','confirm_password','is_supervisor','is_manager','is_occupant',  'token']
    