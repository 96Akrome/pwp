from django import forms
from prueba.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')
        
class UsuarioForm(forms.ModelForm):
     class Meta():
         model = Usuario
         fields = ()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['title', 'cover']