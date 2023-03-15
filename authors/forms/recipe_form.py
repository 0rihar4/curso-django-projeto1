from collections import defaultdict

from django import forms
from django.forms import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr, add_placeholder
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_attr(self.fields['title'], 'Label', 'Receita:')
        add_placeholder(self.fields['title'], 'Nome da Receita')
        add_attr(self.fields['description'], 'Label', 'Descrição:')
        add_attr(self.fields['preparation_steps'], 'class', 'span-2')
        add_placeholder(self.fields['description'], 'Descrição da Receita')
        add_attr(self.fields['preparation_time'], 'Label', 'Tempo de Preparo:')
        add_placeholder(self.fields['preparation_time'], 'Tempo de preparo')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover', 'category')
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                        ('Porções', 'Porções'),
                        ('Pratos', 'Pratos'),
                        ('Pessoas', 'Pessoas'),
                        ('Anões', 'Anões'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                        ('Minutos', 'Minutos'),
                        ('Horas', 'Horas'),
                        ('Dias', 'Dias'),
                )
            ),
            'preparation_time': forms.NumberInput(),
            'servings': forms.NumberInput(),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        frist_char_title = title[0]
        description = cleaned_data.get('description')
        if len(title) < 5:
            self._my_errors['title'].append('Titulo esta muito curto')

        if frist_char_title * len(title) == title:
            self._my_errors['title'].append('Formato invalido do titulo')

        if len(description) < 10:
            self._my_errors['description'].append('Descrição esta muito curto')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Você deve atribuir um '
                                                       'valor positivo')
        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not is_positive_number(servings):
            self._my_errors['servings'].append('Você deve atribuir um '
                                               'valor positivo')
        return servings
