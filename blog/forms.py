from django import forms

class RawSearch(forms.Form):
    search = forms.CharField()