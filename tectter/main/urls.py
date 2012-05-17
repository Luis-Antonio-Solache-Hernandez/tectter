from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^accounts/login/$', 'login', name='login'),
    url(r'^perfil/(?P<username>[a-zA-Z0-9\\_\\.]+)/$', 'show_perfil', name='show_perfil'),
    url(r'^perfil/(?P<username>[a-zA-Z0-9\\_\\.]+)/edit/$', 'edit_perfil', name='edit'),
)
