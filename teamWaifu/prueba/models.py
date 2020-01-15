from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Waifus(models.Model):
    nombre = models.CharField(max_length = 100, blank = False, null = True)
    waifu_card = models.ImageField(upload_to='waifus',blank=False, null = True)
    def __str__(self):
        return self.nombre

class Owned(models.Model):
    created = models.DateTimeField(auto_now_add = True, editable=False)
    creator = models.ForeignKey(User, related_name = "waifu_owner_set", on_delete = models.CASCADE)
    waifu = models.ForeignKey(Waifus, related_name = "waifu_set", on_delete = models.CASCADE)
    def __str__(self):
        return self.waifu.nombre

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add = True, editable=False)
    creator = models.ForeignKey(User, related_name = "friendship_creator_set", on_delete = models.CASCADE)
    friend = models.ForeignKey(User, related_name = "friend_set", on_delete = models.CASCADE)
    def __str__(self):
        return self.friend.username
 
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.user.username

class ProfilePic(models.Model):
    owner = models.ForeignKey(User, related_name = "user_set", on_delete = models.CASCADE)
    title = models.TextField()
    cover = models.ImageField(upload_to='perfil/profile_pics')
    def __str__(self):
        return self.title

class Money(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    money = models.IntegerField()
    def __str__(self):
        return str(self.money)
    

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Usuario.objects.create(user = kwargs['instance'])
        
post_save.connect(create_profile, sender=User)