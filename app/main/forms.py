from django import forms
from django.forms import ModelForm, TextInput



FILTERS = (
    ('time', 'Дата и время'),
    ('total_sum', 'Сумма'),
    ('category', 'Категория')
)

ATTRS = {'class': 'form-control'}


class ReplenishmentForm(forms.Form):
    replenishment = forms.FloatField(min_value=0.0, label='Пополнение баланса', help_text='Введите сумму пополнения баланса',
                                     widget=TextInput(attrs={'class': ATTRS['class']}))


class FilterForm(forms.Form):
    filter_choice = forms.ChoiceField(label='Категория сортировки', choices=FILTERS,)
    flag_choice = forms.BooleanField(label='Сортировать по возрасатнию', initial=True, required=False,
                                     help_text='По умолчанию сортировка осуществляется по убыванию')


class TransactionCreationForm(forms.Form):
    total_sum = forms.FloatField(min_value=0.0, label='Сумма транзакции', help_text='Введите сумму транзакции...',
                                 widget=TextInput(attrs={'class': ATTRS['class']}))
    time = forms.DateTimeField(label='Дата и время транзакции', help_text='Введите дату и время транзакции')
    category = forms.ChoiceField(label='Категории', )



class CategoryCreationForm(forms.Form):
    name = forms.CharField(label='Имя категории', help_text='Введите имя категории', max_length=100,
                           widget=TextInput(attrs={'class': ATTRS['class'], 'placeholder': 'Категория...'}))
