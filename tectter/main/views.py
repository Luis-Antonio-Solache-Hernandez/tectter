from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from main.models import Perfil, Tweet
from main.forms import PerfilForm


@login_required
def index(request):
    try:
        perfil = Perfil.objects.get(user=request.user)
        seguidores = Perfil.objects.filter(friend=perfil).count()
    except Perfil.DoesNotExist:
        perfil = request.user.get_profile()
        seguidores = 0
    return render_to_response('index.html', {
        'perfil': perfil,
        'seguidores': seguidores,
        }, RequestContext(request))


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                menerror = 'No te haz registrado, por favor registrate'
                return render_to_response('login.html', {
        'form': form, 'menerror': menerror,
        }, RequestContext(request))
        password = request.POST['password']
        user = auth.authenticate(username=user.username, password=password)
        form = AuthenticationForm(None, request.POST)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('index')
    return render_to_response('login.html', {
        'form': form,
        }, RequestContext(request))


@login_required
def show_perfil(request, username):
    user = User.objects.get(username=username)
    perfil = Perfil.objects.get(user=user)
    tweets = Tweet.objects.filter(name=perfil)
    try:
        siguiendo = Perfil.objects.get(user=request.user, friend=perfil)
        siguiendo = True
    except Perfil.DoesNotExist:
        siguiendo = False
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': request.user,
        'siguiendo': siguiendo,
        'tweets': tweets,
    }, RequestContext(request))


@login_required
def edit_perfil(request, username):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = PerfilForm(instance=perfil)
    tweets = Tweet.objects.filter(name=perfil)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': request.user,
        'tweets': tweets,
    }, RequestContext(request))
    return render_to_response('add_perfil.html', {
        'form': form,
        }, RequestContext(request))


def seguir(request):
    username = request.POST['username']
    user = User.objects.get(username=username)
    perfil = Perfil.objects.get(user=user)
    perfilactual = Perfil.objects.get(user=request.user)
    try:
        Perfil.objects.get(user=request.user, friend=perfil)
        perfilactual.friend.remove(perfil)
    except Perfil.DoesNotExist:
        perfilactual.friend.add(perfil)
    return redirect('show_perfil', username)
