from django.forms.widgets import TextInput,EmailInput,Select,PasswordInput
from django import forms

from users.models import Users


class SignInForm(forms.Form):
    username = forms.EmailField(widget=EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=200, widget=PasswordInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}))


class SignUpForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['name','email','role','nationality','country','phone','password']

        widgets = {
                'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
                'nationality': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Nationality'}),
                'country': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Country'}),
                'phone': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Phone'}),
                'password': PasswordInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}),
                'email': EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'Email'}),
                'role' : Select(attrs={'class':'form-select',}),
            }