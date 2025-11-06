from django.db import models
from resources.models import Resource
class User(models.Model):
    id = models.AutoField(primary_key=True) 
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    profile_info = models.TextField(blank=True, null=True)


class LastSeen(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource= models.ForeignKey(Resource,on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True)

