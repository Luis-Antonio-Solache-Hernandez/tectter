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
        siguiendo = perfil.friend.filter(public=True) | perfil.friend.filter(public=False, friend__in=[perfil])
        tweets = Tweet.objects.filter(name__id__in=siguiendo) | Tweet.objects.filter(name=perfil)
    except Perfil.DoesNotExist:
        perfil = request.user.get_profile()
        seguidores = 0
        tweets = False
    return render_to_response('index.html', {
        'perfil': perfil,
        'seguidores': seguidores,
        'tweets': tweets,
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
    nseguidores = Perfil.objects.filter(friend=perfil).count()
    perfilactual = Perfil.objects.get(user=request.user)
    try:
        siguiendo = Perfil.objects.get(user=request.user, friend=perfil)
        siguiendo = True
    except Perfil.DoesNotExist:
        siguiendo = False
    try:
        mesigue = Perfil.objects.get(user=perfil, friend=perfilactual)
        mesigue = True
    except Perfil.DoesNotExist:
        mesigue = False
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': request.user,
        'siguiendo': siguiendo,
        'mesigue': mesigue,
        'tweets': tweets,
        'ntweets': tweets.count(),
        'nseguidores': nseguidores
    }, RequestContext(request))


@login_required
def edit_perfil(request, username):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = PerfilForm(instance=perfil)
    tweets = Tweet.objects.filter(name=perfil)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
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


@login_required
def seguidores(request, username):
    user = User.objects.get(username=username)
    perfil = Perfil.objects.get(user=user)
    seguidores = Perfil.objects.filter(friend=perfil)
    perfilactual = Perfil.objects.get(user=request.user)
    myfriends = perfilactual.friend.all()
    nseguidores = Perfil.objects.filter(friend=perfil).count()
    ntweets = Tweet.objects.filter(name=perfil).count()
    try:
        siguiendo = Perfil.objects.get(user=request.user, friend=perfil)
        siguiendo = True
    except Perfil.DoesNotExist:
        siguiendo = False
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': request.user,
        'siguiendo': siguiendo,
        'seguidores': seguidores,
        'myfriends': myfriends,
        'nseguidores': nseguidores,
        'ntweets': ntweets,
    }, RequestContext(request))


@login_required
def siguiendo(request, username):
    user = User.objects.get(username=username)
    perfil = Perfil.objects.get(user=user)
    sig = perfil.friend.all()
    perfilactual = Perfil.objects.get(user=request.user)
    myfriends = perfilactual.friend.all()
    nseguidores = Perfil.objects.filter(friend=perfil).count()
    ntweets = Tweet.objects.filter(name=perfil).count()
    try:
        siguiendo = Perfil.objects.get(user=request.user, friend=perfil)
        siguiendo = True
    except Perfil.DoesNotExist:
        siguiendo = False
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
        'useractual': request.user,
        'siguiendo': siguiendo,
        'sig': sig,
        'myfriends': myfriends,
        'nseguidores': nseguidores,
        'ntweets': ntweets,
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
    return redirect(request.META['HTTP_REFERER'])


def tweetear(request):
    status = request.POST['status']
    perfil = Perfil.objects.get(user=request.user)
    Tweet.objects.create(name=perfil, status=status)
    return redirect('index')


def delete_tweet(request, pk):
    Tweet.objects.filter(pk=pk).delete()
    return redirect(request.META['HTTP_REFERER'])
