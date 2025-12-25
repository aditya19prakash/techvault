from django.db import models
from django.contrib.auth.models import  User
from resources.models import Resource 
from comments.models import Comment

class Resource_votes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    vote = models.CharField(max_length=8)
   

class Comments_votes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment,on_delete=models.CASCADE)
    vote = models.CharField(max_length=8)