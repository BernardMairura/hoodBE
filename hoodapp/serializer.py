from rest_framework import serializers
from django.contrib.auth import get_user_model as user_model
User = user_model()
from .models import *

#create serializer models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name','email','is_superuser','is_admin','is_resident',)

class SuperuserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SuperuserProfile
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdminProfile
        fields = '__all__'

class NeighborhoodSerializer(serializers.ModelSerializer):
    admin = AdminSerializer()

    class Meta:
        model = Neighborhood
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


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'