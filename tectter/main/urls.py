from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^accounts/login/$', 'login', name='login'),
    url(r'^twitt/add/$', 'add_twitt', name='add_twitt'),
)
