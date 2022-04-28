from collections import defaultdict

from apps.recipes.models import Recipe
from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')
        
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', \
            'servings', 'servings_unit', 'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
            
        if title == description:
            self.my_errors['title'].append('Não pode ser igual a descrição')
            self.my_errors['description'].append('Não pode ser igual ao título')
            
        if self.my_errors:
            raise ValidationError(self.my_errors)
        
        return super_clean

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Precisa ser um número positivo')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Precisa ser um número positivo')

        return field_value
