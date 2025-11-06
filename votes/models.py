from django.db import models
from users.models import User
from resources.models import Resource 
class Votes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    vote = models.CharField(max_length=7,default="upvote")
   

