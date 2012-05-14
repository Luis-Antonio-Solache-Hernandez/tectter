from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
#from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User


@login_required
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        #if '@' in request.POST['username']:
         #   username = User.objects.get(email=username)
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            auth.login(request, user)
            return redirect('index')
    return render_to_response('login.html', {
        'form': form,
        }, RequestContext(request))
