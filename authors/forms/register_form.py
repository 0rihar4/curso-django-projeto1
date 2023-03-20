from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    # É recomendavel escolher apenas um metodo para sobreescrever os campos
    # aqui vemos dois metodos um no init e outro dentro do meta, pelo menos
    # é recomendavel usar apenas um metodo por campo, então averigue se vc
    # não esta fazendo isso para por exemplo o username agora no init
    # e novamente dentro do meta
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Digite seu nome:')
        add_attr(self.fields['last_name'], 'Label', 'Sobrenome:')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome:')
        add_placeholder(self.fields['email'], 'Digite seu email:')

    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu nome'},
        required=True,
        label='Nome:'
    )

    username = forms.CharField(
        label='Login:',
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',  # noqa
        error_messages={
            'required': 'Esse campo não pode ser vazio',
            'max_length': 'Esse ultrapassou o limite de 64 caracteres',
            'min_length': 'Digite um username valido',
        },
        widget=forms.TextInput(attrs={
                'placeholder': 'Digite o seu login'
            }),
        max_length=64, min_length=4

    )

    password = forms.CharField(
            required=True,
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha:'
            }),
            label='Senha:',
            error_messages={
                'required': 'Esse campo não pode ficar vazio',
            },
            validators=[strong_password],
            help_text='Sua senha deve conter no minimo 6 caracteres, com no minimo 1 letra maiuscula'  # noqa = E501
        )
    password2 = forms.CharField(
            required=True,
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Repita sua senha:'
            }),
            label='Repita sua senha:',
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
            'username': 'Login:',
            'last_name': 'Sobrenome:',
            'email': 'e-mail:',

        }
        help_text = {
            'email': 'The e-mail must be valid.'
        }
        error_messages = {
            'last_name': {
                'required': 'Esse campo não pode ser vazio 2222',
                'max_length': 'Esse ultrapassou o limite de 64 caracteres',
            }
        }

        # Para placeholders, css, attrs, etc.
        widgets = {
            'username': forms.TextInput(attrs={
                # é possivel personalizar todos attrs do input ate criar
                'class': 'input text-input outra-classe',
                'name': 'username_input',
                'test': 'attr_teste'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha:',
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Esse email ja esta cadastrado!', code='invalid',
            )

        return email

    # o metodo clean sozinho valida o formulario como todo, mas por ordem de
    # execução ele sera executado sempre apos os metodo clean_nome_do_campo

    def clean(self):
        # no metodo clean podemos pegar todos os campos do formulario usando o
        # super dele, como feito abaixo.
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        last_name = cleaned_data.get('last_name')

        if last_name is None:
            raise ValidationError('last_name')
        if password != password2:
            password_confirmation_error = ValidationError(
                'Sua senha não condiz com a digitada '
                'no campo de repetição',
                code='invalid',
                params={'senha1': password, 'senha2': password2}
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            }

            )
