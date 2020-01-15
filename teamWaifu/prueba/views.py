
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, now
from django.contrib import auth
from django.contrib.auth.models import User
from prueba.models import *
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from prueba.forms import UserForm,UsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import os
from django.conf import settings
import random

# from models.py import Usuario
# Create your views here.

def inicio(request):
    user =  request.user
    money = ""
    if request.user.is_authenticated:

        
        print(ProfilePic.objects.filter(owner= user).first())
        try:
            queryCheck = ProfilePic.objects.filter(owner= user).first()
            print("queryCheck funciona")
        except:
            queryCheck = None
            print("nada de nada")
        try:
            queryMoney = Money.objects.filter(owner= user).first()
            
            if request.method == 'POST':
                # Agregar money
                chance = random.choice(range(10))
                queryMoney.money += chance
                queryMoney.save()

            money = queryMoney.money
        except:
            a = 1

    else:
        queryCheck = None
    return render(request, 'inicio.html', {'profile_pic': queryCheck, 'money': money}) 

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


""" def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/perfil')

        else:
            form = UserCreationForm()
            args = {'form': form}
            return render(request, 'register.html', args)
 """
""" 
def register(request):
    registered = False
    
    if request.method == 'POST':

        username = request.POST.get('username')
        pwd = request.POST.get('password')
        confirm_pwd =request.POST.get('confirm')

        user_form = UserForm(data=request.POST)
        profile_form = UsuarioForm(data=request.POST)

        fieldvalue_dict = {}
        fieldvalue_dict["username"] = username
        fieldvalue_dict["pwd"] = pwd

        can_proceed = True
        error_message = ''

        # Revisa que no esten en blanco
        if not username.strip() and can_proceed == True:
            can_proceed = False
            error_message = 'Please enter Username.'

        if not pwd.strip() and can_proceed == True:
            can_proceed = False
            error_message = 'Please enter password.'

        if not confirm_pwd.strip() and can_proceed == True:
            can_proceed = False
            error_message = 'Please confirm password.'


        # Revisa que haya imagen
        profile_picture = request.FILES
        print(profile_picture)

        if 'profile_pic' in profile_picture.keys():
            print('profile pic exists.')

        else:
            print('no pic.')
            profile_picture = None
            can_proceed = False



        if can_proceed == True :
            # Revisa si el usuario ya existe
            user_by_user_name = None
            try:
                user_by_user_name = User.objects.get(username=username)
            except:
                can_proceed = True
            if user_by_user_name:

                can_proceed = False
                error_message = 'Username already exists.'

            # Si todo va bien, crea el usuario usando el modelo de django y crea un userProfilo usando el modelo definido en models
            if can_proceed == True:

                pic = request.FILES['profile_pic']

                user = User.objects.create_user(username=username,password=pwd)
                user_profile = UserProfile.objects.create(profile_pic= pic,user =user)
                #user_profile = UserProfile(user, pic)

                registered = True
                
                return render(request,"registration.html",
                            {'user':user,
                            'user_profile':user_profile,
                            'registered':registered})
            else:
                print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UsuarioForm()

    return render(request,"registration.html",
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})
    """ 


def register(request):
    registered = False
    money = ""
    profile_pic = ""
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UsuarioForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
            usuario = request.POST.get('username')
            # Se le añade dinero al usuario
            queryUser = User.objects.filter(username = usuario).first()
            dinero = Money(owner=queryUser, money = 50)
            dinero.save()
            # User money
            queryMoney = Money.objects.filter(owner= queryUser).first()
            if request.method == 'POST':
                # Agregar money
                print(request.POST)
                if request.POST.get('moneymaker.y'):
                    chance = random.choice(range(10))
                    queryMoney.money += chance
                    queryMoney.save()

            # Se le agrega foto al usuario:
            if 'profile_pic' in request.FILES:
                print('found it')
                profile_pic = request.FILES['profile_pic']

                ext = profile_pic.name.split('.')[-1]
                profile_pic.name = "%s.%s" % (queryUser.username, ext)
            
                try:
                    os.remove(settings.MEDIA_ROOT + "/perfil/profile_pics/"+ profile_pic.name)
                except:
                    a = 1            
                ProfilePic.objects.filter(owner=queryUser).delete()

                foto = ProfilePic(owner=queryUser, title = profile_pic.name, cover=profile_pic)
                foto.save()
                            # Prepara la imagen para mostrar en html
                try:
                    profile_pic = ProfilePic.objects.filter(owner= queryUser).first()
                except:
                    profile_pic = None

            money = queryMoney.money
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UsuarioForm()
    return render(request,"registration.html",
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered, 
                           'money': money,
                           'profile_pic' : profile_pic })

def user_login(request):
    queryCheck = None
    if request.method == 'POST':
        if request.POST.get('Login'):
            print(request.method)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    print(ProfilePic.objects.filter(owner= user).first())
                    try:
                        queryCheck = ProfilePic.objects.filter(owner= user).first()
                        print("queryCheck funciona")
                    except:
                        queryCheck = None
                        print("nada de nada")

        if request.user.is_authenticated:
            nombre = request.user    
            # User money
            queryMoney = Money.objects.filter(owner= nombre).first()
            # Agregar money
            print(request.POST)
            if request.POST.get('moneymaker.y'):
                chance = random.choice(range(10))
                queryMoney.money += chance
                queryMoney.save()
            money = queryMoney.money
            return render(request, "login2.html", {'profile_pic': queryCheck, 'money':money})
            
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Los datos ingresados no son validos")
    else:
        return render(request, "login2.html", {'profile_pic': queryCheck})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/inicio')



@login_required(login_url='/login')
def vista_perfil(request):
    user = request.user
    friendAdd = False
    try:
        queryFriends = Friendship.objects.filter(creator=username)
    except:
        queryFriends = None
    
    try:
        queryWaifus = Owned.objects.filter(creator=username)
    except:
        queryWaifus = None

    if request.method == 'POST':
        #Friend request
        friend_req = request.POST.get('friend')
        try:
            queryUser = User.objects.filter(username = friend_req).first()
            try:
                queryFriend = Friendship.objects.filter(creator = user, friend = queryUser).first()
                print("queryCheck funciona: "+ queryFriend.username)
            except:
                queryCheck = None
                print("aun no son amigos, pero ahora lo seran")
                amistad = Friendship(creator=user, friend = queryUser)
                amistad.save()
        except:
            print("fail, amigo no existe, forever alone")


        #Profile pic
        if 'profile_pic' in request.FILES:
            print('found it')
            profile_pic = request.FILES['profile_pic']

            ext = profile_pic.name.split('.')[-1]
            profile_pic.name = "%s.%s" % (user.username, ext)
        
            try:
                os.remove(settings.MEDIA_ROOT + "/perfil/profile_pics/"+ profile_pic.name)
            except:
                a = 1            
            ProfilePic.objects.filter(owner=user).delete()

            foto = ProfilePic(owner=user, title = profile_pic.name, cover=profile_pic)
            foto.save()

    # Prepara la imagen para mostrar en html
    try:
        queryCheck = ProfilePic.objects.filter(owner= user).first()
    except:
        queryCheck = None

    # Prepara para mostrar amigos en html
    
    queryFriend = Friendship.objects.filter(creator = user)
    amistad = []
    amigos = []
    if queryFriend is not None:
        for amigo in queryFriend:
            if len(amigos) < 5:
                amigos.append(amigo.friend.username)
            else:
                amistad.append(amigos)
                amigos = []
                amigos.append(amigo.friend.username)

    if len(amigos) > 0:
        amistad.append(amigos)


    
    # Prepara para mostrar waifus en html

    queryWaifu = Owned.objects.filter(creator = user)
    coleccion = []
    waifus = []
    if queryWaifu is not None:
        for waifu in queryWaifu:
            if len(waifus) < 5:
                waifus.append(waifu.waifu.nombre)
            else:
                coleccion.append(waifus)
                waifus = []
                waifus.append(waifu.waifu.nombre)
            
    if len(waifus) > 0:
        coleccion.append(waifus)

    # User money
    queryMoney = Money.objects.filter(owner= user).first()
    if request.method == 'POST':
        # Agregar money
        print(request.POST)
        if request.POST.get('moneymaker.y'):
            chance = random.choice(range(10))
            queryMoney.money += chance
            queryMoney.save()
    money = queryMoney.money
    print(coleccion)

    return render(request, "perfil.html",
                            {'amigos':amistad, 
                             'waifus':coleccion,
                             'profile_pic':queryCheck,
                             'money':money})

    
@login_required(login_url='/login')
def gacha(request):
    # User money
    user = request.user
    elegida = ""
    queryMoney = Money.objects.filter(owner= user).first()

    if request.method == 'POST':
        # Agregar money
        print(request.POST)
        money = queryMoney.money

        if request.POST.get('moneymaker.y'):
            chance = random.choice(range(10))
            queryMoney.money += chance
            queryMoney.save()
            money = queryMoney.money


        
        if request.POST.get('gacha'):
            if money >= 50:
                todasLasWaifus = Waifus.objects.all()
                print(todasLasWaifus)
                elegida = random.choice(todasLasWaifus)
                print(elegida)
                #Genera waifu
                felicidad = Owned(creator = user, waifu = elegida)
                felicidad.save()
                queryMoney.money -= 50
                queryMoney.save()
                money = queryMoney.money



    money = queryMoney.money
    return render(request, 'gacha.html',
                            {'money': money,
                             'waifu': elegida})

