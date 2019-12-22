from django.db import models
from django.utils import timezone
# Create your models here.

 
class Item(models.Model):
    nombre = models.CharField(max_length = 100, verbose_name = "Elemento", blank = False, null = True)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return u'%s' % self.nombre

class Waifus(models.Model):
    ident = models.IntegerField()
    def __str__(self):
        return u'%s' % self.ident

class Friends(models.Model):
    ident = models.IntegerField()
    def __str__(self):
        return u'%s' % self.ident

class Usuario(models.Model):
    user = models.CharField(max_length = 30, verbose_name = "Username", blank = False, null = False)
    inventario = models.ForeignKey(Waifus, on_delete = models.CASCADE, blank = True, null = True)
    amigos = models.ForeignKey(Friends, on_delete = models.CASCADE, blank = True, null = True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return u'%s' % self.user