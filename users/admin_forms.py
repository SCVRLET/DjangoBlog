from django import forms

from .models import User, Post

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'login',
            'email',
            'password',
            'token',
            'is_admin'
        )
        widgets = {
            'avatar': forms.FileInput,
            'login': forms.TextInput,
            'email': forms.EmailInput,
            'password': forms.TextInput,
            'token': forms.TextInput,
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'text',
            'created_at',
        )

        widgets = {
            'user_id': forms.TextInput
        }