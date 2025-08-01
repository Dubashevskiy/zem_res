from land.models import LandPlot
from django import forms
from django.forms import DateInput
import django_filters
from django_filters import DateFromToRangeFilter, RangeFilter
from django_filters.widgets import RangeWidget

class WaterForm(forms.ModelForm):
    cadastr_number = forms.CharField(required=True,
                                     label="Кадастровий номер",
                                     widget=forms.TextInput(attrs={'class': 'form-control'})
                                     )
    location = forms.CharField(required=True,
                               label='Місцезнаходження земельної ділянки',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    area = forms.DecimalField(required=True,
                              label='Площа, га',
                              widget=forms.NumberInput(attrs={'class': 'form-control'})
                              )
    coordinates = forms.CharField(required=False,
                               label='Координати',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )

    owner_name = forms.CharField(required=False,
                                 label='Користувач',
                                 widget=forms.TextInput(attrs={'class': 'form-control'})
                                 )
    destination = forms.ChoiceField(required=True,
                                    label='Цільове призначення',
                                    choices=[('', '')] + LandPlot.DESTINATION_CHOICES,
                                    widget=forms.Select(attrs={'class': 'form-control'})
                                    )
    rent_start = forms.DateField(
        required=False,
        label='Дата реєтрації',
        input_formats=['%d.%m.%Y'],
        widget=DateInput(
            attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y')
    )
    rent_end = forms.DateField(
        required=False,
        label='Термін дії',
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y'))

    interest = forms.DecimalField(required=False,
                                  label='Відсоток',
                                  widget=forms.NumberInput(attrs={'class': 'form-control'})
                                  )
    assessment = forms.DecimalField(required=False,
                                    label='Нормативна оцінка',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                                    )
    land = forms.ChoiceField(required=True,
                             label='Угіддя',
                             choices=[('', '')] + LandPlot.LAND_CHOICES,
                             widget=forms.Select(attrs={'class': 'form-control'})
                             )

    notes = forms.CharField(required=False,
                            label='Примітка',
                            widget=forms.TextInput(attrs={'class': 'form-control'})
                            )
    pass_number = forms.DecimalField(required=False,
                                  label='№ реєстру',
                                  widget=forms.NumberInput(attrs={'class': 'form-control'})
                                  )
    pass_name = forms.CharField(required=False,
                            label='Назва папорту',
                            widget=forms.TextInput(attrs={'class': 'form-control'})
                            )
    pass_area = forms.DecimalField(required=False,
                              label='Площа, га',
                              widget=forms.NumberInput(attrs={'class': 'form-control'})
                              )
    pass_volume = forms.DecimalField(required=False,
                              label='Обєм при НПР',
                              widget=forms.NumberInput(attrs={'class': 'form-control'})
                              )
    pass_depth = forms.DecimalField(required=False,
                              label='Глибина, м',
                              widget=forms.NumberInput(attrs={'class': 'form-control'})
                              )
    date_approval = forms.DateField(
        required=False,
        label='Дата погодження',
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y'))

    pass_developer = forms.CharField(required=False,
                            label='Розробник',
                            widget=forms.TextInput(attrs={'class': 'form-control'})
                            )


    class Meta:
        model = LandPlot
        fields = ['cadastr_number', 'area',  'location', 'destination', 'land', 'coordinates', 'owner_name', 'rent_start', 'rent_end', 'interest', 'assessment',  'notes',
                  'pass_number', 'pass_name', 'pass_area', 'pass_volume', 'pass_depth', 'date_approval',  'pass_developer']

class WaterFilterForm(django_filters.FilterSet):
        def assessment_filter(self, queryset, name, value):
            if value == '0':
                return queryset.filter(assessment__isnull=True)  # Порожні
            elif value == '1':
                return queryset.filter(assessment__isnull=False)  # Заповнені
            return queryset

        def interest_filter(self, queryset, name, value):
            if value == '0':
                return queryset.filter(interest__isnull=True)  # Порожні
            elif value == '1':
                return queryset.filter(interest__isnull=False)  # Заповнені
            return queryset

        def passname_filter(self, queryset, name, value):
            if value == '0':
                return queryset.filter(pass_name__isnull=True)  # Порожні
            elif value == '1':
                return queryset.filter(pass_name__isnull=False)  # Заповнені
            return queryset

        cadastr_number = django_filters.CharFilter(
            label='Кадастровий номер',
            lookup_expr='icontains',  # фільтрує за прибизним значенням
            widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
        )
        location = django_filters.CharFilter(
            label='Місцезнаходження',
            lookup_expr='icontains',
            widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle', 'id': 'id_location'})
        )
        area = RangeFilter(
            label='Площа (га) (від - до)',
            widget=RangeWidget(attrs={
                'class': 'form-control border-primary-subtle',
                'placeholder': '0,0000 Га'
            }),
        )
        owner_name = django_filters.CharFilter(
            label='Користувач',
            lookup_expr='icontains',
            widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
        )
        destination = django_filters.ChoiceFilter(
            label='Цільове призначення',
            choices=LandPlot.DESTINATION_CHOICES,
            empty_label="",
            widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
        )
        rent_start = DateFromToRangeFilter(
            label='Дата реєстрації (від - до)',
            lookup_expr='icontains',
            widget=RangeWidget(attrs={
                'type': 'date',
                'class': 'form-control border-primary-subtle'
            })
        )

        rent_end = DateFromToRangeFilter(
            label='Термін дії (від - до)',
            lookup_expr='icontains',
            widget=RangeWidget(attrs={
                'type': 'date',
                'class': 'form-control border-primary-subtle'
            })
        )
        interest = RangeFilter(
            label='Відсоток (від - до)',
            widget=RangeWidget(attrs={
                'class': 'form-control border-primary-subtle'
            })
        )

        assessment = django_filters.CharFilter(
            label='Нормативна оцінка',
            widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
        )

        assess_filter = django_filters.ChoiceFilter(
            label='Нормативна оцінка наявна',
            choices=[(0, 'ні'), (1, 'так')],
            method='assessment_filter',
            empty_label='',
            widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
        )
        land = django_filters.ChoiceFilter(
            label='Угіддя',
            choices=LandPlot.LAND_CHOICES,
            empty_label="",
            widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
        )

        inter_filter = django_filters.ChoiceFilter(
            label='Відсоток наявний',
            choices=[(0, 'ні'), (1, 'так')],
            method='interest_filter',
            empty_label='',
            widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
        )
        pass_name = django_filters.ChoiceFilter(
            label='Паспорт наявний',
            choices=[(0, 'ні'), (1, 'так')],
            method='passname_filter',
            empty_label='',
            widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
        )

        class Meta:
            model = LandPlot
            fields = ['cadastr_number', 'location', 'area', 'destination', 'land', 'coordinates', 'owner_name',
                      'rent_start', 'rent_end', 'interest', 'assessment', 'notes', 'pass_name']

class WaterExcelImportForm(forms.Form):
    file = forms.FileField(label="Завантажити Excel файл (.xlsx)")