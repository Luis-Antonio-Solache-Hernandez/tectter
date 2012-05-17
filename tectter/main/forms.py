from django import forms
from main.models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
