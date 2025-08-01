from django import forms
from .models import LandPlot
from django.forms import DateInput
import django_filters
from django_filters import DateFromToRangeFilter, RangeFilter, ChoiceFilter
from django_filters.widgets import RangeWidget

# форма для додавання в таблицю про оренду
class LeaseAgreementForm(forms.ModelForm):
    def clean_cadastr_number(self):
        data = self.cleaned_data.get('cadastr_number')
        if not data:
            return None  # або просто return data — обережно з NULL

        existing = LandPlot.objects.filter(cadastr_number=data)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("Такий кадастровий номер вже існує.")
        return data

    cadastr_number = forms.CharField( required=False,
                                      label="Кадастровий номер",
                                      widget=forms.TextInput(attrs={'class': 'form-control'})
                                      )
    location = forms.CharField(required=True,
                               label='Місцезнаходження земельної ділянки',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    area = forms.DecimalField (required=True,
                            label='Площа, га',
                            widget=forms.NumberInput(attrs={'class': 'form-control'})
                            )
    coordinates = forms.CharField(required=False,
                               label='Координати',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    status = forms.ChoiceField(required=True,
                               label='Використання',
                                choices=[('', '')] + LandPlot.STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'})
                               )
    owner_name = forms.CharField(required=False,
                               label='Користувач',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    category = forms.ChoiceField(  # або ModelChoiceField, якщо це ForeignKey
        required=True,
        label='Категорія земель',
        choices=[('', '')] + LandPlot.CATEGORY_CHOICES,  # якщо це choices в моделі
        widget=forms.Select(attrs={'class': 'form-control'})
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

    rent_end_max = forms.DateField(
        required=False,
        label='Термін дії',
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y'))

    decision_number = forms.CharField(required=False,
                               label='Номер рішення',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    decision_date = forms.DateField(
        required=False,
        label='Дата рішення',
        input_formats=['%d.%m.%Y'],
        widget=DateInput(
            attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y'))

    interest  = forms.DecimalField (required=False,
                            label='Відсоток',
                            widget=forms.NumberInput(attrs={'class': 'form-control'})
                            )
    assessment = forms.DecimalField (required=False,
                            label='Нормативна оцінка',
                            widget=forms.NumberInput(attrs={'class': 'form-control'})
                            )
    land = forms.ChoiceField(required=True,
                               label='Угіддя',
                              choices=[('', '')] + LandPlot.LAND_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'})
                               )
    registered = forms.ChoiceField(required=False,
                               label='зареєстровано',
                                choices=[('', '')] + LandPlot.REGISTER_CHOICES,
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
    gidr_constr = forms.ChoiceField(required=False,
                               label='Гідроспоруда',
                                choices=[('', '')] + LandPlot.GIDR_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'})
                               )
    gidr_number = forms.IntegerField(required=False,
                              label='№ акта гідроспоруди',
                              widget=forms.NumberInput(attrs={'class': 'form-control'})
                              )
    gidr_coordinates = forms.CharField(required=False,
                               label='Координати гідроспоруди',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    suborendar = forms.ChoiceField(required=False,
                               label='Суборенда',
                                choices=[('', '')] + LandPlot.SUBORENDA_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'})
                               )
    sub_owner_name = forms.CharField(required=False,
                                 label='Суборендар',
                                 widget=forms.TextInput(attrs={'class': 'form-control'})
                                 )
    sub_rent_start = forms.DateField(
        required=False,
        label='Дата реєтрації',
        input_formats=['%d.%m.%Y'],
        widget=DateInput(
            attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y')
        )
    sub_rent_end = forms.DateField(
        required=False,
        label='Термін дії',
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ДД.ММ.РРРР'}, format='%d.%m.%Y'))
    class Meta:
        model = LandPlot
        fields = ['cadastr_number', 'location', 'area', 'status', 'coordinates', 'owner_name', 'category', 'destination', 'rent_start', 'rent_end', 'rent_end_max', 'interest', 'assessment',
                  'land', 'registered', 'notes', 'has_passport', 'pass_number', 'pass_name', 'pass_area', 'pass_volume', 'pass_depth', 'date_approval',  'pass_developer',
                  'gidr_constr', 'gidr_number', 'gidr_coordinates', 'suborendar', 'sub_owner_name', 'sub_rent_start', 'sub_rent_end', 'decision_number', 'decision_date']

class LeaseFilterForm(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"LeaseFilterForm ініціалізовано з data={self.data}")  # Дебаг

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

    def filter_has_passport(self, queryset, name, value):
        if value == 'yes':
            return queryset.filter(has_passport=True)
        elif value == 'no':
            return queryset.filter(has_passport=False)
        return queryset

    def filter_geom(self, queryset, name, value):
        print(f"filter_geom викликано з value={value}, type={type(value)}")  # Дебаг
        if value == '1':
            return queryset.filter(geom__isnull=False)
        elif value == '0':
            return queryset.filter(geom__isnull=True)
        return queryset


    def filter_decision(self, queryset, name, value):
        if value == '0':
            return queryset.filter(decision_number__isnull=True)  # Порожні
        elif value == '1':
            return queryset.filter(decision_number__isnull=False)  # Заповнені
        return queryset


    HAS_PASSPORT_CHOICES = (
        ('yes', 'Так'),
        ('no', 'Ні'),
    )



    cadastr_number = django_filters.CharFilter(
        label='Кадастровий номер',
        lookup_expr='icontains',# фільтрує за прибизним значенням
        widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
    )
    location = django_filters.CharFilter(
        label='Місцезнаходження',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle', 'id': 'id_location'})
    )
    area = RangeFilter(
        label='Площа (га)',
        widget=RangeWidget(attrs={
            'class': 'form-control border-primary-subtle',
            'placeholder': '0,0000 Га'
        }),
    )
    owner_name = django_filters.CharFilter(
        label='Користувач',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle', 'id': 'id_owner_name'})
    )
    category = django_filters.ChoiceFilter(
        label='Категорія земель',
        choices=LandPlot.CATEGORY_CHOICES,
        empty_label="",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )
    destination = django_filters.ChoiceFilter(
                               label='Цільове призначення',
                                choices=LandPlot.DESTINATION_CHOICES,
                                empty_label="",
                               widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
                               )
    rent_start = DateFromToRangeFilter(
        label='Дата реєстрації',
        lookup_expr='range',
        widget=RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control border-primary-subtle'
        })
    )

    rent_end = DateFromToRangeFilter(
        label='Термін дії',
        lookup_expr='range',
        widget=RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control border-primary-subtle'
        })
    )
    interest = RangeFilter(
        label='Відсоток',
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
    status = django_filters.ChoiceFilter(
        label='Тип користування',
        choices=LandPlot.STATUS_CHOICES,
        empty_label="",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )
    registered = django_filters.ChoiceFilter(
        label='Договір зареєстрований',
        choices=LandPlot.REGISTER_CHOICES,
        empty_label="",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )
    suborendar = django_filters.ChoiceFilter(
        label="Суборенда",
        choices=LandPlot.SUBORENDA_CHOICES,
        empty_label="",
        widget = forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )

    sub_owner_name = django_filters.CharFilter(
        label='Суборендар',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
    )
    sub_rent_start = DateFromToRangeFilter(
        label='Дата реєстрації',
        lookup_expr='range',
        widget=RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control border-primary-subtle'
        })
    )

    sub_rent_end = DateFromToRangeFilter(
        label='Термін дії',
        lookup_expr='range',
        widget=RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control border-primary-subtle'
        })
    )

    inter_filter = django_filters.ChoiceFilter(
        label='Відсоток наявний',
        choices=[(0, 'ні'), (1, 'так')],
        method='interest_filter',
        empty_label='',
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )

    decision_number = django_filters.CharFilter(
        label='Номер рішення',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control border-primary-subtle'})
    )

    decision_date = DateFromToRangeFilter(
        label='Дата рішення',
        lookup_expr='range',
        widget=RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control border-primary-subtle'
        })
    )

    decision_filter = django_filters.ChoiceFilter(
        label='Рішення наявне',
        choices=[(0, 'ні'), (1, 'так')],
        method='filter_decision',
        empty_label='',
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )

    has_passport = ChoiceFilter(
        label="Наявність паспорта",
        choices=HAS_PASSPORT_CHOICES,
        method='filter_has_passport',
        empty_label='',
        widget = forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )
    geom_filter = django_filters.ChoiceFilter(
        label='Координати',
        choices=[(0, 'ні'), (1, 'так')],
        method='filter_geom',
        empty_label='',
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )


    class Meta:
        model = LandPlot
        fields = ['cadastr_number', 'location', 'area', 'owner_name', 'category', 'destination',  'interest', 'assessment', 'assess_filter', 'land',
                  'rent_start', 'rent_end', 'registered', 'inter_filter', 'has_passport', 'geom_filter',
                  'suborendar', 'sub_owner_name', 'sub_rent_start', 'sub_rent_end', 'decision_filter', 'decision_date', 'decision_number']
''
class ExcelImportForm(forms.Form):
    file = forms.FileField(label="Завантажити Excel файл (.xlsx)")
