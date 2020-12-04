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
 
   