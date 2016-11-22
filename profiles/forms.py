from django import forms
from profiles.models import SkillCategory


class EditForm(forms.Form):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    city_name = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'city'}))
    lat = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'lat'}))
    lon = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'lon'}))
    country_code = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'country_code'}))


class AddSkillForm(forms.Form):
    skill_name = forms.CharField(max_length=100)
    categories_object = SkillCategory.objects.all()
    category_choices = [(i.id, i.name) for i in categories_object]
    category = forms.ChoiceField(widget=forms.Select, choices=category_choices)
    desc = forms.CharField(widget=forms.Textarea)
