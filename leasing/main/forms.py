from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from.models import *

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'second_name', 'phone', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'second_name': forms.TextInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder':'+7(000)000-00-00'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'})
        }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))

class CreateNewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title', 'description', 'photo', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'text-area'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'select'}),
        }

class CreateServicesForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = ['title', 'description', 'price', 'photo', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'text-area'}),
            'price': forms.NumberInput(attrs={'class': 'input'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'select'}),
        }

class CreateNewsComment(forms.Form):
    description = forms.CharField(label='Ваш комментарий:', widget=forms.Textarea(attrs={'class': 'text-area'}))

class FilterNewsForm(forms.ModelForm):
    class Meta:
        model = CategoriesNews
        fields = ['category']
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'select'})
        }

class FilterServicesForm(forms.ModelForm):
    class Meta:
        model = CategoriesServices
        fields = ['category']
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'select'})
        }