from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'StrongP4$sw0rd',
            'password2': 'StrongP4$sw0rd',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Esse campo não pode ser vazio'),
        ('password', 'Esse campo não pode ficar vazio'),
        ('password2', 'Esse campo não pode ficar vazio'),
        ('first_name', 'Escreva seu nome'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:register_create')
        msg = 'Digite um username valido'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_4(self):
        self.form_data['username'] = 'a'*65
        url = reverse('authors:register_create')
        msg = 'Esse ultrapassou o limite de 64 caracteres'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password2_is_must_be_equal(self):
        self.form_data['password'] = 'aaaa'
        self.form_data['password2'] = 'bbb'
        url = reverse('authors:register_create')
        msg = 'Sua senha não condiz com a digitada no campo de repetição'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_email_field_not_be_duplicate_in_data_base(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        # self.form_data['email'] = 'email@email.com'
        msg = 'Esse email ja esta cadastrado!'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        # Testando a senha fraca
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        msg = 'Sua senha é muito fraca! Ela deve conte 8 caracteres,'
        'sendo uma maiuscula, uma minuscula, um numero',
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        # Testando a senha FORTE
        self.form_data['password'] = '@Abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )
        self.assertTrue(is_authenticated)
