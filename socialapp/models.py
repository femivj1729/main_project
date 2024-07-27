from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=50,blank=True)
    bio=models.TextField(blank=True)
    location=models.CharField(max_length=50,blank=True)
    links=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='pictures',default='blank_profile.jpg')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Likepost(models.Model):
    post_id=models.CharField(max_length=100)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowersCount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return self.user



class Message(models.Model):
    sender=models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name='received_messages',on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content}'
    
    class Meta:
        ordering=['-timestamp']

