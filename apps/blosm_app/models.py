from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re, time
from datetime import date
from bcrypt import hashpw
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
 def register(self, postData):
     error_msgs = []
     try:
         if User.objects.get(username=postData['username']):
             error_msgs.append("Username already in use")
     except:
         pass
     if not re.match(EMAIL_REGEX, postData['email']):
            error_msgs.append("invalid email")
     if len(postData['username']) < 3:
         error_msgs.append("Username is too short")
     if len(postData['password']) < 8:
         error_msgs.append("Password is too short")
     if not postData['password'] == postData['confirm']:
         error_msgs.append("Passwords do not match!")
     if error_msgs:
         return {'errors':error_msgs}
     else:
         hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
         user = User.objects.create(username=postData['username'], email=postData['email'], password=hashed)
         return {'theuser':user.username, 'userid': user.id}
 def login(self, postData):
    error_msgs = []
    password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
    try:
         user = User.objects.get(username=postData['username'])
    except:
        error_msgs.append("Invalid Login Credentials!")
        return {'errors': error_msgs}
    if not bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password.encode():
        error_msgs.append("Incorrect password.")
    if error_msgs:
        return {'errors':error_msgs}
    else:
        return {'theuser':user.username, 'userid':user.id}

class AlbumManager(models.Manager):
    def createAlbum(self, postData, id):
        error_msgs = []
        if len(postData['albumtitle']) < 3:
            error_msgs.append("Username is too short")
        else:
            print id
            album = Album.objects.create(albumtitle=postData['albumtitle'], albumreleasedate=postData['albumreleasedate'], user_id = User.objects.get(id=id))
            print album.id
            return {'albumid': album.id}
    def deleteAlbum(self, id):
		Album.objects.get(id=id).delete()
                print id
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Album(models.Model):
    albumtitle = models.CharField(max_length=255)
    albumreleasedate = models.DateTimeField()
    albumart = models.ImageField(upload_to='album_image', blank=True)
    user_id = models.ForeignKey(User)
    objects = AlbumManager()
