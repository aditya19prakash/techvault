from django.db import models
from django.contrib.auth.models import  User
from resources.models import Resource
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    resource =models.ForeignKey(Resource,on_delete=models.CASCADE)
    content = models.CharField(max_length=500,null= False,blank = False) 
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,null= True,blank= True,related_name="replies")

    def __str__(self):
        return f"id ={self.id} name={self.user.username} - {self.content[:30]}"