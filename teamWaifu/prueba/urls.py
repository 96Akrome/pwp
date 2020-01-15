from django.conf.urls import url, include
from prueba.views import *
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

# SET THE NAMESPACE!
app_name = 'prueba'
 
urlpatterns = [
    url(r"^$",inicio),
    url(r"^inicio/$",inicio),
    url(r"^descripcion/$",descripcion),
    url(r"^login/$",loginn),
    #url(r"^login/logueado/",vista_logueado),
    
    url(r"^register/$",register),
    url(r"^user_login/$",user_login),
    url(r'^logout/$', user_logout),
    url(r'^perfil/$',vista_perfil),
    url(r'^gacha/$',gacha),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)