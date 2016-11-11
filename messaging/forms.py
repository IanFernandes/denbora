from django import forms


class MessageForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    msg_content = forms.CharField(widget=forms.Textarea)
