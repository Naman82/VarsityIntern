from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
import os, uuid

class User(AbstractUser):
    username = None
    USER_TYPE_CHOICES = [
        (0, 'Admin'),
        (1, 'User'),
    ]
    email = models.EmailField(_('email address'), unique=True, null=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    def get_update_filename(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('uploads/user/profile', filename)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    name = models.CharField(max_length=255,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to=get_update_filename, default='uploads/user/profile/default_profile.jpg')

    def __str__(self):
        return "{},{}".format(str(self.name),str(self.user))