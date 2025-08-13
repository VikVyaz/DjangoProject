from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField

from mailing.forms import StyleFormMixin

from .models import User


class UserRegisterFrom(StyleFormMixin, UserCreationForm):
    phone_number = PhoneNumberField(verbose_name='Номер телефона', max_length=15, blank=True, null=True)
    usable_password = None

    placeholder_data = {
        'email': 'Email пользователя',
        'password': 'Пароль пользователя',
        'username': 'Ник пользователя',
        'password1': 'Придумайте пароль',
        'password2': 'Повторите пароль'
    }
    form_class_data = {
        'country': 'form-select',

    }

    class Meta:
        model = User
        fields = ('email', 'username', 'avatar', 'phone_number', 'country', 'password1', 'password2')


class CustomAuthForm(StyleFormMixin, AuthenticationForm):
    placeholder_data = {
        'username': 'Email пользователя',
        'password': 'Пароль пользователя'
    }

    class Meta:
        model = User
        fields = ('email', 'password')


User_for_update = get_user_model()


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    new_password1 = forms.CharField(required=False, label='Новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=False, label='Повторите новый пароль', widget=forms.PasswordInput)
    placeholder_data = {
        'username': 'Ник пользователя',
        'email': 'Email пользователя',
        'new_password1': 'Новый пароль(необязательно)',
        'new_password2': 'Повторите новый пароль',
    }

    def clean(self):
        cleaned_data = super().clean()
        pswrd1 = cleaned_data.get('new_password1')
        pswrd2 = cleaned_data.get('new_password2')

        if pswrd1 and pswrd1 != pswrd2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('new_password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User_for_update
        fields = ('email', 'username', 'avatar', 'phone_number', 'country')
