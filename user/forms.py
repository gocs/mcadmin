from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, Payment

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

# PlayerForm these players are whitelisted
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['id', 'uuid']

# PaymentForm these are the payments made by the players
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['player', 'amount']
