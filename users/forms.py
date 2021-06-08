import hashlib

from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputEmail', 'placeholder': 'E-mail'}))
    login = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputLogin', 'placeholder': 'Login'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputConfirmPassword', 'placeholder': 'Confirm password'}))

    field_order = ['email', 'login', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'There is a user with this e-mail!')

        return email
    

    def clean_login(self):
        login = self.cleaned_data['login']

        if User.objects.filter(login=login).exists():
            raise forms.ValidationError(f'There is a user with such login!')
        
        return login


    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.confirm_password

        if password != confirm_password:
            raise forms.ValidationError(f'"Password" and "Confim password" inputs are not the same')
        
        return password


class UserSignInForm(forms.Form):
    login = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'SignInInputLogin', 'placeholder': 'Login'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'SignInInputPassword', 'placeholder': 'Password'}))
    
    field_order = ['login', 'password']

    def clean_login(self):
        login = self.cleaned_data['login']

        if not User.objects.filter(login=login).exists():
            raise forms.ValidationError(f'There are no users with such login!')
        
        return login

    
    def clean_password(self):
        password = self.cleaned_data['password']
        password_hash = hashlib.md5(password.encode()).hexdigest()
        login = self.cleaned_data.get('login')

        if not User.objects.filter(login=login, password=password_hash).exists():
            raise forms.ValidationError(f'Wrong login or password')

        return password