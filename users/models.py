from django.db import models
from resources.models import Resource
from django.contrib.auth.models import  User

class User_history(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource,null=False,blank=False,on_delete=models.CASCADE)
    
    user = models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    timestamp = models.TimeField(auto_now_add=True)