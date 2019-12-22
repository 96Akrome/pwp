from django import forms
from prueba.models import Usuario
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
class UsuarioForm(forms.ModelForm):
     class Meta():
         model = Usuario
         fields = ('profile_pic',)