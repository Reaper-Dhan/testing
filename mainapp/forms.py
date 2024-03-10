# forms.py (create this file if it doesn't exist)
from django import forms

class FlagVerificationForm(forms.Form):
    flag = forms.CharField(label='Flag', max_length=100)
