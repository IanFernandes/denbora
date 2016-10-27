from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())