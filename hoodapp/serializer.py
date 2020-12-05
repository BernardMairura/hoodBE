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

class OccupantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = OccupantProfile
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Business
        fields = '__all__'
