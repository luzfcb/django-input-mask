import json

import six
from django import forms
from django.conf import settings


def mask_cls(widget_cls, js=None, mask=None, data_attrs=None):
    if mask is None:
        mask = {}

    _mask = mask

    class InputMask(widget_cls):
        mask = None

        _js = js
        _data_attrs = data_attrs or {}

        def __init__(self, **kwargs):
            # read mask from kwargs
            self.original_maxlength = None
            mask = self._parse_mask_attr(kwargs.pop('mask', {}))

            super(InputMask, self).__init__(**kwargs)

            # read mask from function
            for k, v in self._parse_mask_attr(_mask).items():
                mask[k] = v

            # update self.mask
            if self.mask is None:
                self.mask = {}

            for k, v in mask.items():
                self.mask[k] = v

        def render(self, name, value, attrs=None):
            attrs = attrs or {}
            for attr, cb in self._data_attrs.items():
                attrs[attr] = cb(self)
            return super(InputMask, self).render(name, value, attrs=attrs)

        @property
        def media(self):
            return forms.Media(js=self._js)

        def _parse_mask_attr(self, mask):
            if isinstance(mask, six.string_types):
                return {'mask': mask}
            return mask

        def get_context(self, *args, **kwargs):
            context = super(InputMask, self).get_context(*args, **kwargs)
            return context

        def build_attrs(self, *args, **kwargs):
            """Build an attribute dictionary."""
            attrs = super(InputMask, self).build_attrs(*args, **kwargs)
            if 'maxlength' in attrs and self.mask:
                maxlength = int(attrs['maxlength'])
                self.original_maxlength = maxlength
                len_mask = len(self.mask.get('mask', maxlength))
                if maxlength < len_mask:
                    attrs['maxlength'] = str(len_mask)
            return attrs

    return InputMask


def mask(widget_cls, extra_js=None, data_attrs=None, **kwargs):
    cls = input_mask(widget_cls, extra_js=extra_js, data_attrs=data_attrs)
    return cls(**kwargs)


def input_mask_encode_options(opts):
    return json.dumps(opts).replace('"', "'")[1:-1]


def input_mask(widget_cls, extra_js=None, **kwargs):
    js = (
        settings.STATIC_URL + 'input_mask/js/inputmask/inputmask.js',
        settings.STATIC_URL + 'input_mask/js/inputmask/jquery.inputmask.js',
        settings.STATIC_URL + 'input_mask/js/inputmask/inputmask.binding.js',
    ) + (extra_js or ())

    kwargs['data_attrs'] = {
        'data-inputmask': lambda self: input_mask_encode_options(self.mask),
    }

    return mask_cls(widget_cls, js=js, **kwargs)


def input_mask_decimal(widget_cls, **kwargs):
    extra_js = (
        settings.STATIC_URL + 'input_mask/js/inputmask/inputmask.extensions.js',  # noqa
        settings.STATIC_URL + 'input_mask/js/inputmask/inputmask.numeric.extensions.js',  # noqa
    )

    return input_mask(widget_cls, extra_js=extra_js, **kwargs)


def money_mask_encode_options(opts):
    return json.dumps(opts).replace('"', '&quot;')


def money_mask(widget_cls, **kwargs):
    js = (
        settings.STATIC_URL + 'input_mask/js/jquery.maskMoney.min.js',
        settings.STATIC_URL + 'input_mask/js/text_input_mask.js',
    )

    kwargs['data_attrs'] = {
        'data-money-mask': lambda self: money_mask_encode_options(self.mask),
    }

    return mask_cls(widget_cls, js=js, **kwargs)


def decimal_mask(widget_cls, mask=None):
    return money_mask(widget_cls, mask=mask)
