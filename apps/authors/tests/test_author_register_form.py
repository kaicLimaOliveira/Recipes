from turtle import setup

from authors.forms import RegisterForm
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Digite seu usuário'),
        ('email', 'Seu e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Digite sua senha'),
        ('password2', 'Repita sua senha'),
    ])
    def test_first_name_placeholder_is_correct(self, field, placeholder):    
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        
        self.assertEqual(current_placeholder, placeholder)
        
    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.O tamanho deve ser entre 4 e 150 caracteres'),
        ('email', 'Digite um e-mail valido')
    ])
    def test_fields_help_text(self, field, needed):    
        form = RegisterForm()
        current = form[field].field.help_text
        
        self.assertEqual(current, needed)
        
    @parameterized.expand([
        ('username', 'Usuario'),
        ('email', 'E-mail'),
        ('first_name', 'Primeiro Nome'),
        ('last_name', 'Ultimo Nome'),
        ('password', 'Password'),
        ('password2', 'Password2')
    ])
    def test_fields_label(self, field, needed):    
        form = RegisterForm()
        current = form[field].field.label
        
        self.assertEqual(current, needed)
    
class AuthorRegisterFormIntegrationtest(TestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@any.com',
            'password': 'StrongP@ssword1',
            'password2': 'StrongP@ssword1'
        }
        
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.O tamanho deve ser entre 4 e 150 caracteres'),
    ])
    def test_fields_cannoty_be_empty(self, field, msg):
        self.form_data[field] = ''
        
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn(msg, response.content.decode('utf-8'))
        
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Seu usuario tem menos de 4 caracteres'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Seu usuario tem mais de 150 caracteres'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Senha é fraca. Sua senha deve conter: Pelo menos uma letra minuscula e um numero 8 caracteres'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas não são iguais'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_field_must_be_unique(self):
        url = reverse('authors:register_create')
        
        self.client.post(url, data=self.form_data, follow=True)
        
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Um usuário com este nome de usuário já existe.'

        self.assertIn(msg, response.content.decode('utf-8'))
        # self.assertIn(msg, response.context['form'].errors.get('email'))

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
