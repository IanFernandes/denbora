from django import forms


class EditForm(forms.Form):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=True)
    city = forms.CharField(max_length=255, required=False)
    city_name = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'city'}))
    lat = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'lat'}))
    lon = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'lon'}))
    country_code = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'country_code'}))
