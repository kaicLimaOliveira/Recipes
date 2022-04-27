import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val
    
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError(
            (
                'Senha é fraca. '
                'Sua senha deve conter: '
                'Pelo menos uma letra minuscula e um numero '
                '8 caracteres'
            ),
            code='invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')
        
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
        label='Password'
    )
    
    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(),
        label='Password2'
    )
    
    username = forms.CharField(
        label='Usuario',
        help_text=(
            'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
            'O tamanho deve ser entre 4 e 150 caracteres'
        ),
        error_messages={
            'required': 'O campo está vazio',
            'min_length': 'Seu usuario tem menos de 4 caracteres',
            'max_length': 'Seu usuario tem mais de 150 caracteres',
        },
        min_length=4, max_length=150,
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
        # exclude = ['first_name']
        labels = {
            'username': 'Usuario',
            'first_name': 'Primeiro Nome',
            'last_name': 'Ultimo Nome',
            'email': 'E-mail'
        }
        
        help_texts = {
            'email': 'Digite um e-mail valido',
        }
        
        error_messages = {
            'username': {
                'required': 'Esse campo é Obrigatório',
            }
        },
        
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input text-input',
            })
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                'password':'As senhas não são iguais',
                'password2':'As senhas não são iguais'
            })