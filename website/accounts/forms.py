from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    code = forms.CharField(max_length=20, required=False, label='Код купона',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['count', 'email', 'payment_method']
        widgets = {
            'count': forms.TextInput(attrs={'class': 'form-control',
                                            'type': 'number',
                                            'min': '1',
                                            'value': '1'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'custom-select mb-2 mr-sm-2 mb-sm-0'})
        }
