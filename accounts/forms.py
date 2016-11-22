from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username...', 'class': 'form-control'}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email...', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password...', 'class': 'form-control'}))
    password_repeat = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password...', 'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password...', 'class': 'form-control'}))
