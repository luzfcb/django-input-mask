from django import forms
from django.conf import settings
from django.utils import numberformat
from django.utils.safestring import mark_safe
from django.utils.formats import get_format
from django.utils import translation
from django.contrib.staticfiles import finders

from json import dumps
from decimal import Decimal

from .utils import chunks


__all__ = (
    'InputMask',
    'DecimalInputMask',
)


class InputMask(forms.TextInput):
    def __init__(self, *args, **kwargs):
        mask = kwargs.pop('mask', {})
        super(InputMask, self).__init__(*args, **kwargs)
        self.mask.update(mask)

    def render(self, name, value, attrs=None):
        if hasattr(self, 'mask'):
            if self.mask.get('type') != 'reverse':
                class_ = 'mask '
            else:
                class_ = 'mask mask-reverse '

            #class_ += dumps(self.mask).replace('"', '&quot;')
            class_ += dumps(self.mask).replace("'", '&quot;')

            final_attrs = self.build_attrs(self.attrs, type=self.input_type, name=name)
            if 'class' in final_attrs:
                attrs['class'] = u'%s %s' % (final_attrs['class'], mark_safe(class_))
            else:
                attrs['class'] = mark_safe(class_)

        return super(InputMask, self).render(name, value, attrs=attrs)

    class Media:
        js = (
            settings.STATIC_URL + 'input_mask/js/jquery19support.js',
            settings.STATIC_URL + 'input_mask/js/jquery.metadata.js',
            settings.STATIC_URL + 'input_mask/js/jquery.meio.mask.min.js',
            settings.STATIC_URL + 'input_mask/js/text_input_mask.js',
        )


class DecimalInputMask(InputMask):
    mask = {
        'type': 'reverse',
        'defaultValue': '000',
    }

    thousands_sep = get_format('THOUSAND_SEPARATOR')
    decimal_sep = get_format('DECIMAL_SEPARATOR')

    def __init__(self, max_digits=10, decimal_places=2, *args, **kwargs):
        super(DecimalInputMask, self).__init__(*args, **kwargs)

        self.max_digits = max_digits
        self.decimal_places = decimal_places

    def render(self, name, value, attrs=None):
        self.mask['mask'] = '%s%s%s' % (
            '9' * self.decimal_places,
            self.decimal_sep,
            chunks(
                '9' * (self.max_digits - self.decimal_places), 3,
                self.thousands_sep),
        )

        try:
            Decimal(value)
        except:
            pass
        else:
            value = numberformat.format(
                value,
                self.decimal_sep,
                decimal_pos=self.decimal_places,
                thousand_sep=self.thousands_sep,
            )

        return super(DecimalInputMask, self).render(name, value, attrs=attrs)



default_date_format = getattr(settings, 'DATE_INPUT_FORMATS', None)
if default_date_format:
    default_date_format = str(default_date_format[0])

def get_language():
    lang = translation.get_language()
    if '-' in lang:
        lang = '%s-%s' % (lang.split('-')[0].lower(), lang.split('-')[1].upper())
    return lang


def get_locale_js_url(lang):
    url = 'datepicker/js/locales/bootstrap-datepicker.%s.js' % lang
    if finders.find(url):
        return settings.STATIC_URL + url
    if '-' in lang:
        return get_locale_js_url(lang.split('-')[0].lower())
    return ''


def javascript_date_format(python_date_format):
    js_date_format = python_date_format.replace(r'%Y', 'yyyy')
    js_date_format = js_date_format.replace(r'%m', 'mm')
    js_date_format = js_date_format.replace(r'%d', 'dd')
    if '%' in js_date_format:
        js_date_format = ''
    if not js_date_format:
        js_date_format = 'yyyy-mm-dd'
    return js_date_format




class BootstrapDateInputMask(InputMask, forms.DateInput):

    bootstrap = {
        'append': mark_safe('<i class="icon-calendar"></i>'),
        'prepend': None,
    }

    @property
    def media(self):
        js = (
            settings.STATIC_URL + 'datepicker/js/bootstrap-datepicker.js',
        )
        lang = get_language()
        if lang != 'en':
            locale_js_url = get_locale_js_url(lang)
            if locale_js_url:
                js = js + (
                    locale_js_url,
                )
        js = js + (
            settings.STATIC_URL + 'bootstrap_toolkit/js/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'datepicker/css/datepicker.css',
            )
        }
        return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        date_input_attrs = {}
        if attrs:
            date_input_attrs.update(attrs)
        date_format = self.format
        if not date_format:
            date_format = default_date_format
        date_input_attrs.update({
            'data-date-format': javascript_date_format(date_format),
            'data-date-language': get_language(),
            'data-bootstrap-widget': 'datepicker',
        })
        return super(BootstrapDateInputMask, self).render(name, value, attrs=date_input_attrs)



default_date_format = getattr(settings, 'DATE_INPUT_FORMATS', None)
if default_date_format:
    default_date_format = str(default_date_format[0])


def get_language():
    lang = translation.get_language()
    if '-' in lang:
        lang = '%s-%s' % (lang.split('-')[0].lower(), lang.split('-')[1].upper())
    return lang


def get_locale_js_url(lang):
    url = 'input_mask/js/datepicker/locales/bootstrap-datepicker.%s.js' % lang
    if finders.find(url):
        return settings.STATIC_URL + url
    if '-' in lang:
        return get_locale_js_url(lang.split('-')[0].lower())
    return ''


def javascript_date_format(python_date_format):
    js_date_format = python_date_format.replace(r'%Y', 'yyyy')
    js_date_format = js_date_format.replace(r'%m', 'mm')
    js_date_format = js_date_format.replace(r'%d', 'dd')
    if '%' in js_date_format:
        js_date_format = ''
    if not js_date_format:
        js_date_format = 'yyyy-mm-dd'
    return js_date_format


def meiomask_date_format(python_date_format):
    meiomask = python_date_format.replace(r'%Y', '9999')
    meiomask = meiomask.replace(r'%m', '19')
    meiomask = meiomask.replace(r'%d', '39')
    if '%' in meiomask:
        meiomask = ''
    if not meiomask:
        meiomask = '9999/19/39'
    return meiomask


class BootstrapDateInputMask(forms.DateInput, InputMask):
    mask = {
        'mask': meiomask_date_format(default_date_format),
    }

    def __init__(self, *args, **kwargs):
        super(BootstrapDateInputMask, self).__init__(*args, **kwargs)
        self.mask['mask'] = meiomask_date_format(self.format)


    bootstrap = {
        'append': mark_safe('<i class="glyphicon glyphicon-calendar"></i>'),
        'prepend': None,
    }

    @property
    def media(self):
        js = (
            settings.STATIC_URL + 'input_mask/js/datepicker/bootstrap-datepicker.js',
        )
        lang = get_language()
        if lang != 'en':
            locale_js_url = get_locale_js_url(lang)
            if locale_js_url:
                js = js + (
                    locale_js_url,
                )
        js = js + (
            settings.STATIC_URL + 'input_mask/js/datepicker/init_datepicker.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'input_mask/css/datepicker/datepicker.css',
            )
        }
        return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        date_input_attrs = {}
        if attrs:
            date_input_attrs.update(attrs)
        date_format = self.format
        if not date_format:
            date_format = default_date_format
        date_input_attrs.update({
            'data-date-format': javascript_date_format(date_format),
            'data-date-language': get_language(),
            'data-bootstrap-widget': 'datepicker',
        })
        return super(BootstrapDateInputMask, self).render(name, value, attrs=date_input_attrs)

