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
        user = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        user = request.user.get_profile()
    return render_to_response('index.html', {
        'user': user,
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
    useractual = Perfil.objects.get(user=request.user)
    friend = Perfil.objects.filter(friend=perfil)
    friend = [perfil.friend for perfil in friend]
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': useractual,
        'siguiendo': (perfil in friend),
        'tweets': tweets,
    }, RequestContext(request))


@login_required
def edit_perfil(request, username):
    user = get_object_or_404(Perfil, user=request.user)
    form = PerfilForm(instance=user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render_to_response('add_perfil.html', {
        'form': form,
        }, RequestContext(request))


def seguir(request):
    username = request.POST['username']
    user = User.objects.get(username=username)
    perfiluser = Perfil.objects.get(user=user)
    perfilactual = Perfil.objects.get(user=request.user)
    siguiendo = perfilactual.friend.all()
    if perfiluser in siguiendo:
        perfilactual.friend.remove(perfiluser)
    else:
        perfilactual.friend.add(perfiluser)
    perfil = Perfil.objects.get(user=user)
    tweets = Tweet.objects.filter(name=perfil)
    useractual = request.user
    friend = Perfil.objects.filter(friend=perfil)
    friend = [perfil.friend for perfil in friend]
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': useractual,
        'siguiendo': (perfil in friend),
        'tweets': tweets,
        }, RequestContext(request))
