from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'Label', 'Login:')
        add_placeholder(self.fields['username'], 'Digite seu login')
        add_attr(self.fields['password'], 'Label', 'Login:')
        add_placeholder(self.fields['password'], 'Digite sua senha')

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
