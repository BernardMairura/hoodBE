import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import datetime, timedelta







class AdminProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='hood_administrator')
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True)
    bio = models.TextField(max_length=100, blank=True)
    prof_picture= CloudinaryField('image',blank=True,null=True)
    contact = models.CharField(max_length=15, blank=True)
    date_created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.first_name 


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:  
            if instance.is_manager:  
                AdminProfile.objects.create(user=instance) 

            else:
                pass


class SuperuserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='hood_administrator')
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    bio = models.TextField(max_length=100, blank=True)
    prof_picture= CloudinaryField('image',blank=True,null=True)
    contact = models.CharField(max_length=15, blank=True)
    date_created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name 


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:  
            if instance.is_manager:  
                SuperuserProfile.objects.create(user=instance) 

            else:
                pass
    