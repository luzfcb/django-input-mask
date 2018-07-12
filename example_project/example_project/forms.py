from django import forms

from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput
from input_mask.fields import DecimalField
from input_mask.fields import MoneyField as OriginalMoneyField
from input_mask.utils import mask
from input_mask.widgets import InputMask

class PhoneNumberMask(InputMask):
    mask = {'mask': '999-999-9999', 'placeholder': 'XXX-XXX-XXXX'}


class SSNMask(InputMask):
    mask = {'mask': '999-99-9999'}


class BRPhoneNumberMask(InputMask):
    mask = {'mask': '(99)[9]9999-9999'}


class CPFMask(InputMask):
    mask = {'mask': '999.999.999-99'}


class BRPhoneNumberInput2(BRPhoneNumberInput):

    def __init__(self, **kwargs):
        super(BRPhoneNumberInput2, self).__init__(**kwargs)




class MoneyField(OriginalMoneyField):
    def __init__(self, *args, **kwargs):
        mask = {
            'precision': 0,
            'allowZero': False,
            'prefix': '$',
            'affixesStay': True,
        }

        mask.update(kwargs.pop('mask', {}))

        super(MoneyField, self).__init__(mask=mask, *args, **kwargs)


class BasicForm(forms.Form):
    decimal_field = DecimalField(max_digits=10, decimal_places=2)
    money_field = MoneyField(mask={'precision': 2})
    phone_number = forms.CharField(widget=PhoneNumberMask)
    ssn = forms.CharField(widget=SSNMask)
    date = forms.CharField(
        widget=mask(forms.DateInput,
                    mask='99/99/9999',
                    attrs={
                        'placeholder': 'MM/DD/YYYY',
                    },
                    format='%m/%d/%Y'))
    date2 = forms.DateField(
        widget=mask(forms.DateInput,
                    mask='99/99/9999',
                    attrs={
                        'placeholder': 'MM/DD/YYYY',
                    },
                    format='%m/%d/%Y')
    )
    cpf = forms.CharField(widget=CPFMask)
    telefone = forms.CharField(widget=BRPhoneNumberMask)

    br_data_nascimento = forms.DateField(
        widget=mask(
            widget_cls=forms.DateInput,
            mask='99/99/9999',
            attrs={
                'placeholder': 'MM/DD/YYYY',
            },
            format='%m/%d/%Y')
    )

    def clean(self):
        c = super(BasicForm, self).clean()
        print(c)
        return c
