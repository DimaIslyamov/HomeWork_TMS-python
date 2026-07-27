from django import forms


class DemoRequestForm(forms.Form):
    student = forms.CharField()
    course = forms.CharField()
    