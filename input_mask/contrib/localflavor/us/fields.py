from decimal import Decimal

from ....fields import DecimalField
from .widgets import USDecimalInput


class USDecimalField(DecimalField):
    widget = USDecimalInput

    def to_python(self, value):
        return Decimal(value)
