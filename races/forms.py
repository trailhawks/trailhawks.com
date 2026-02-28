from django import forms

from .models import Race


class RaceChatForm(forms.Form):
    race = forms.ModelChoiceField(
        queryset=Race.objects.all().order_by("-start_datetime"),
        label="Race",
        widget=forms.Select(attrs={"class": "block w-full rounded-md border-gray-300 shadow-sm"}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "class": "block w-full rounded-md border-gray-300 shadow-sm",
                "rows": 3,
                "placeholder": "Ask about this race or request changes...",
            }
        ),
    )


class RaceAgentForm(forms.Form):
    race = forms.ModelChoiceField(
        queryset=Race.objects.all().order_by("-start_datetime"),
        label="Race",
        widget=forms.Select(attrs={"class": "block w-full rounded-md border-gray-300 shadow-sm"}),
    )
    url = forms.URLField(
        label="URL",
        widget=forms.URLInput(
            attrs={
                "class": "block w-full rounded-md border-gray-300 shadow-sm",
                "placeholder": "https://ultrasignup.com/register.aspx?did=...",
            }
        ),
    )
