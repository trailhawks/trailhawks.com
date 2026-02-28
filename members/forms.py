from django import forms


class ContactForm(forms.Form):
    message = forms.CharField()
    sender = forms.EmailField()
