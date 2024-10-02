from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import CustomUser
from django import forms

class LoginForm(forms.Form):

    email = forms.CharField(label="Email", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    field = ('email', 'password')
    def auth(self, request):
        auth_email = self.cleaned_data.get('email')
        pword = self.cleaned_data.get('password')
        return authenticate(request, username=auth_email, password=pword)

alphabet = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabet characters are allowed.')

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(label="First name", required=True, validators=[alphabet], widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last name", required=True, validators=[alphabet],widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))   

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

class EditForm(forms.ModelForm):

    first_name = forms.CharField(label="First name", required=True, validators=[alphabet], widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last name", required=True, validators=[alphabet], widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name')