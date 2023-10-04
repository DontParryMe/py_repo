from django import forms


class OrderForm(forms.Form):
    customer = forms.EmailField(max_length=255)
    model = forms.CharField(max_length=2)
    version = forms.CharField(max_length=2)
