# from django.test import TestCase
from unittest import TestCase

from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitest(TestCase):

    @parameterized.expand(
        [
            ('first_name', 'Digite seu nome:'),
            ('last_name', 'Digite seu sobrenome:'),
            ('username', 'Digite o seu login'),
            ('password', 'Digite sua senha:'),
            ('password2', 'Repita sua senha:'),
            ('email', 'Digite seu email:'),
        ]
    )
    def test_fields_placeholder_is_correct(self, field, needed):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, needed)

    @parameterized.expand(
        [
            ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),  # noqa
            ('password', 'Sua senha deve conter no minimo 6 caracteres, com no minimo 1 letra maiuscula'),  # noqa
            ('password2', 'Repita sua senha exatamente igual a digitada no campo anterior'),  # noqa
        ]
    )
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand(
        [
            ('first_name', 'Nome:'),
            ('last_name', 'Sobrenome:'),
            ('username', 'Login:'),
            ('password', 'Senha:'),
            ('password2', 'Repita sua senha:'),
            ('email', 'e-mail:'),
        ]
    )
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
