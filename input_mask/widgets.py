from django import forms

from .utils import decimal_mask, input_mask

__all__ = (
    'InputMask',
    'DecimalInputMask',
)


InputMask = input_mask(forms.TextInput)


class DecimalInputMask(decimal_mask(forms.TextInput)):
    pass
