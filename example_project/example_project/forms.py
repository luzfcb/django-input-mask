from django import forms

from input_mask.fields import DecimalField
from input_mask.widgets import BootstrapDateInputMask

class BasicForm(forms.Form):
    decimal_field = DecimalField(max_digits=10, decimal_places=2)
    date_field = forms.DateField(
        widget=BootstrapDateInputMask()
    )
