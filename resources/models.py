from django.db import models
from users.models import User 

class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tech_stack = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(blank=True,null=True)      

    def __str__(self):
        return self.title
