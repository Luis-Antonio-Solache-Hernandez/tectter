from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='img', default='img/User.png')
    birth_date = models.DateField(auto_now=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    public = models.BooleanField(default=True)
    biography = models.TextField(max_length=50, blank=True, null=True)
    friend = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return '%s' % self.user.username


def get_profile(user):
    if not hasattr(user, '_profile_cache'):
        profile, created = Perfil.objects.get_or_create(user=user, name=user.username)
        user._profile_cache = profile
    return user._profile_cache
User.get_profile = get_profile


class Tweet(models.Model):
    name = models.ForeignKey("Perfil", related_name='tweet')
    status = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.status
