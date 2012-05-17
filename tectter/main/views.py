from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from main.models import Perfil
from main.forms import PerfilForm


@login_required
def index(request):
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


def add_perfil(request):
    form = PerfilForm()
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render_to_response('add_perfil.html', {
        'form': form,
    }, RequestContext(request))


@login_required
def show_perfil(request, username):
    perfil = Perfil.objects.get(user=request.user)
    return render_to_response('show_perfil.html', {
        'perfil': perfil,
    })


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
