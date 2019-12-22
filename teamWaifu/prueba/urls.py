from django.conf.urls import url, include
from prueba.views import *

# SET THE NAMESPACE!
app_name = 'prueba'
 
urlpatterns = [
    url(r"^$",inicio),
    url(r"^inicio/$",inicio),
    url(r"^descripcion/$",descripcion),
    url(r"^login/$",loginn),
    url(r"^login/logueado/",vista_logueado),
    
    url(r"^register/$",register),
    url(r"^user_login/$",user_login),
    url(r'^logout/$', user_logout),
]
