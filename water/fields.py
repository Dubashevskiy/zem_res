from django import forms
import django_filters
from django_filters import Filter


# Кастомне поле, яке замінює кому на крапку
class CommaDecimalField(forms.DecimalField):
    def clean(self, value):
        if isinstance(value, str):
            value = value.replace(',', '.')
        return super().clean(value)

# Кастомний RangeFilter, який використовує наше поле
class CommaDecimalRangeFilter(django_filters.RangeFilter):
    field_class = CommaDecimalField