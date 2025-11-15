from django.db import models
from resources.models import Resource
class Ai_summary(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    summary = models.TextField(blank=False,null=False)
    def __str__(self):
        return self.resource

class Ai_saved_answer(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE,null=False,blank=False)
    question = models.CharField(max_length=1000)
    answer = models.TextField(null=False,blank=False)
