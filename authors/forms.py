import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(passowrd):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(passowrd):
        raise ValidationError(
            'Sua senha %(senha)s é muito fraca! Ela deve conte 8 caracteres,'
            'sendo uma maiuscula, uma minuscula, um numero',
            code='min_lenght',
            params={'senha': passowrd}
        )


class RegisterForm(forms.ModelForm):
    # É recomendavel escolher apenas um metodo para sobreescrever os campos
    # aqui vemos dois metodos um no init e outro dentro do meta, pelo menos
    # é recomendavel usar apenas um metodo por campo, então averigue se vc
    # não esta fazendo isso para por exemplo o username agora no init
    # e novamente dentro do meta
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['first_name'], 'Label', 'Nome')
        add_placeholder(self.fields['first_name'], 'Digite seu nome:')
        add_attr(self.fields['last_name'], 'Label', 'Sobrenome:')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome:')

    password = forms.CharField(
            required=True,
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha'
            }),
            label='Digite sua senha',
            error_messages={
                'required': 'Esse campo não pode ficar vazio',
            },
            validators=[strong_password],
            help_text='Sua senha deve conter no minimo 6 caracteres, com no minimo 1 letra maiuscula'  # noqa = E501
        )
    password2 = forms.CharField(
            required=True,
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Repita sua senha'
            }),
            label='Repita sua senha',
            error_messages={
                'required': 'Esse campo não pode ficar vazio',
            },
            help_text='Repita sua senha exatamente igual a digitada no campo anterior'  # noqa = E501
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Login',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'e-mail',

        }
        help_text = {
            'email': 'The e-mail must be valid.'
        }
        error_messages = {
            'usernamre': {
                'required': 'Esse campo não pode ser vazio',
                'max_length': 'Esse ultrapassou o limite de 64 caracteres',
            }
        }

        # Para placeholders, css, attrs, etc.
        widgets = {
            'username': forms.TextInput(attrs={
                # é possivel personalizar todos attrs do input ate criar
                'placeholder': 'Digite o seu login',
                'class': 'input text-input outra-classe',
                'name': 'username_input',
                'test': 'attr_teste'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha',
                'show': 'show',
            }),

        }

    # Para validar campos separadamente basta usar o metodo nativo do django
    # clean_nome_do_campo()
    def clean_password(self):
        # pegando os campos do formulario com cleaned_data
        data = self.cleaned_data.get('password')
        if len(data) < 8:
            raise ValidationError(
                'Sua senha %(senha)s é muito curta!',
                code='min_lenght',
                params={'senha': data}
            )
        return data
    # o metodo clean sozinho valida o formulario como todo, mas por ordem de
    # execução ele sera executado sempre apos os metodo clean_nome_do_campo

    def clean(self):
        # no metodo clean podemos pegar todos os campos do formulario usando o
        # super dele, como feito abaixo.
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Sua senha %(senha1)s não condiz com a %(senha2)s',
                code='invalid',
                params={'senha1': password, 'senha2': password2}
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            }

            )
