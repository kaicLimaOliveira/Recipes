from turtle import setup
from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

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
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
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
        ('username', 'Esse campo é Obrigatório'),
        ('first_name', ''),
        ('last_name', ''),
    ])
    def test_fields_cannoty_be_empty(self, field, msg):
        self.form_data[field] = ''
        
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn(msg, response.content.decode('utf-8'))
        
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))