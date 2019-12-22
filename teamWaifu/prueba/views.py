
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, now
from django.contrib import auth
from django.contrib.auth.models import User
from prueba.models import Waifus, Item, Friends, Usuario
from django.contrib.auth.decorators import login_required
from prueba.forms import UserForm,UsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# from models.py import Usuario
# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def descripcion(request):
    context = {'nombre':localtime(now())}
    return render(request, 'descripcion.html', context)

def loginn(request): #logea super user
    if request.method == 'POST':
        if ("username" in  request.POST.keys()) and ("password" in  request.POST.keys()):
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect("/inicio/logueado/")
            else:
                contexto={"error":"error"}
                return render(request,"login.html",contexto)
        else:
            contexto={"error":"error"}
            return render(request,"login.html",contexto)
    return render(request,"login.html")


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UsuarioForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UsuarioForm()
    return render(request,"registration.html",
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return render(request, "inicio.html")
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, "login2.html", {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/inicio')


@login_required(login_url='/login')
def vista_logueado(request):
    if request.method =='POST':
        if ("cerrar" in request.POST.keys()):
            auth.logout(request)
            return redirect("/login/")
        if ("perfil_home" in request.POST.keys()):
            return render(request, 'perfil.html')    
    return render(request, 'user_login.html')

# @login_required(login_url='/login')
# def vista_perfil(request):
#     contexto = {"Usuario":request.user}
#     return render(request, 'perfil.html',contexto)
