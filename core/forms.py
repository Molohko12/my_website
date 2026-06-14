from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['static_field', 'full_name', 'age', 'department']
        labels = {
            'static_field': 'Статик',
            'full_name': 'Имя фамилия',
            'age': 'Сколько вам лет',
            'department': ''
        }
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
        }