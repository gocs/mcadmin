from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full'})
        self.fields['password1'].widget.attrs.update({'class': 'w-full'})
        self.fields['password2'].widget.attrs.update({'class': 'w-full'})

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "w-full"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "w-full"}))

