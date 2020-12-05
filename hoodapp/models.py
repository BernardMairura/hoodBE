
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import datetime, timedelta







class AdminProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
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
            if instance.is_admin:  
                AdminProfile.objects.create(user=instance) 

            else:
                pass


class SuperuserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
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
            if instance.is_superuser:  
                SuperuserProfile.objects.create(user=instance) 

            else:
                pass
    

class OccupantProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True)
    location=models.CharField(max_length=30,blank=True)
    bio =models.TextField(max_length=100, blank=True)
    prof_picture= CloudinaryField('image')
    contact = models.CharField(max_length=15, blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    hoodname = models.ForeignKey("Neighborhood", on_delete=models.CASCADE,related_name='home', null=True)

    def __str__(self):
        return self.full_name 


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:  
            if instance.is_occupant:  
                OccupantProfile.objects.create(user=instance) 

            else:
                pass


class Neighborhood(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    location = models.CharField(max_length=60)
    admin = models.ForeignKey("AdminProfile", on_delete=models.CASCADE)
    hoodphoto = CloudinaryField('image')
    body= models.TextField(max_length=100, blank=True)
    resident_count= models.IntegerField(null=True, blank=True)
    emergency_contact = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'neighborhood'
    

    def __str__(self):
        return f'{self.name} neighborhood'

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)



class Business(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    body = models.TextField(max_length=100, blank=True)
    hood_id = models.ForeignKey("Neighborhood", on_delete=models.CASCADE, related_name='business')
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, related_name='neighbor_profile')
    location = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:  
            if instance.is_manager:  
                Business.objects.create(user=instance) 

            else:
                pass