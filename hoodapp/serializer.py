from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import *

#create serializer models

class SuperuserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperuserProfile
        fields = '__all__'
