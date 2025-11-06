from django.db import models
from users.models import User
from resources.models import Resource
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resource =models.ForeignKey(Resource,on_delete=models.CASCADE)
    content = models.CharField(max_length=500,null= False,blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,null= True,blank= True,related_name="replies")
    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"