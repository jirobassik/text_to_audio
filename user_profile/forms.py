from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    email = forms.EmailField(required=True, label='Почта')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        password2_data = cd['password2']
        if cd['password'] != password2_data:
            self.add_error('password', forms.ValidationError('Пароли не совпадают'))
        return password2_data

    def clean_email(self):
        cd = self.cleaned_data['email']
        if User.objects.filter(email=cd).exists() and not self.has_error('username'):
            self.add_error('username',
                           forms.ValidationError('Неправильное сочетание имени пользователя, пароля и почты'))
        return cd

    def clean_username(self):
        cd = self.cleaned_data['username']
        if User.objects.filter(username=cd).exists():
            self.add_error('username',
                           forms.ValidationError('Неправильное сочетание имени пользователя, пароля и почты'))
        return cd
