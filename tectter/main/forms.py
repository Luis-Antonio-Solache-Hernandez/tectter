from django import forms
from main.models import Perfil, Tweet


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('image', 'name', 'birth_date', 'city', 'public', 'biography',)


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('status',)
