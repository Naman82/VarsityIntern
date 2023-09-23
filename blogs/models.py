from django.db import models
from users.models import User

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title  = models.CharField(max_length = 255)
    meta_title = models.CharField(max_length = 255 , null=True,blank=True)
    body = models.TextField()
    timeStamp = models.DateTimeField(auto_now = True)
    tags = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.user)
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField()
    timeStamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)