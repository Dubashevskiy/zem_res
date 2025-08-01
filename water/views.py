from django.shortcuts import render, redirect, get_object_or_404
from land.models import LandPlot
from .forms import WaterFilterForm, WaterForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from .filters import WaterFilter
import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from datetime import datetime
import json
from django.utils.html import format_html
from django.db.models import Q
from .fields import CommaDecimalField, CommaDecimalRangeFilter


# Create your views here.


# додавання договору
def water_add(request):
    if request.method == 'POST':
        form = WaterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ інформація додана!')
            return redirect('water')  # назад до списку
    else:
        form = WaterForm()
    return render(request, 'water/water_add.html', {'form': form, 'title': 'Нова інформація про став'})

# фільтр
def water_filter(request):
    water_plots = LandPlot.objects.all()
    water_filter = WaterFilter(request.GET, queryset=water_plots)

    paginator = Paginator(water_filter.qs, 5)  # або скільки хочеш
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('water/water_result.html', {
            'leases': page_obj,
            'page_obj': page_obj,
        })
        return JsonResponse({'html': html})

    return render(request, 'water/water.html', {
        'filter': water_filter,
        'leases': page_obj,
        'page_obj': page_obj,
    })

# редагування договору
def water_edit(request, pk):
    lease = get_object_or_404(LandPlot, pk=pk)
    if request.method == "POST":
        form = WaterForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Внесено зміни успішно!')
            query_string = request.META.get('QUERY_STRING', '')
            return redirect(f'{reverse("water_result")}?{query_string}')
    else:
        form = WaterForm(instance=lease)
    return render(request, 'water/water_edit.html',
                  {'form': form,
                        'title': 'Редагувати запис',
                        'lease': lease,})

# видалення договору
def water_delete(request, pk):
    lease = get_object_or_404(LandPlot, pk=pk)
    lease.delete()
    messages.success(request, '❌ Ділянка видалена!')
    return redirect('water')

# історія змін
# порівняння рядків
def get_changes(prev, curr):
    changes = []
    for field in curr._meta.fields:
        field_name = field.name
        # Пропускаємо службові поля
        if field_name in ['id', 'history_id', 'history_date', 'history_user', 'history_type']:
            continue
        old = getattr(prev, field_name, None)
        new = getattr(curr, field_name, None)
        if old != new:
            verbose_name = field.verbose_name.capitalize()
            changes.append((verbose_name, old, new))
    return changes

def water_history(request, pk):
    land_plot = get_object_or_404(LandPlot, pk=pk)
    history = land_plot.history.all().order_by('-history_date')

    history_with_changes = []
    for i in range(len(history) - 1):
        current = history[i]
        previous = history[i + 1]
        changes = get_changes(previous, current)
        history_with_changes.append((current, changes))

    # Додаємо перший запис (створення)
    if history:
        history_with_changes.append((history.last(), []))

    return render(request, 'water/water_history.html', {
        'history': history_with_changes
    })

# Пагінація
def water_list(request):
    landplots = LandPlot.objects.all().order_by('id')  # Можна додати фільтрацію

    paginator = Paginator(landplots, 50)  # 20 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'water/water_list.html', {'page_obj': page_obj})

def your_view(request):
    leases = LandPlot.objects.all()
    paginator = Paginator(leases, 50)  # по 10 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "your_template.html", {"page_obj": page_obj})

# експорт Excel
def water_export_excel(request):
    # Створюємо новий Excel файл
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Water"

    # Заголовки
    headers = ["№", "Кадастровий номер", "Площа, га", "Населений пункт", "Цільове призначення", "Угіддя", "Координати", "Користувач",
               "Дата реєстрації", "Термін дії", "Відсоток", "Нормативна оцінка", "Примітка", "№ реєстру", "Назва паспорту",
               "Площа, га", "Обєм при НПР", "Глибина, м", "Дата погодження", "Розробник"]
    sheet.append(headers)
    # Жирний стиль для заголовків
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Дані з моделі
    waters = LandPlot.objects.all()
    cadastr_number = request.GET.get("cadastr_number")
    if cadastr_number:
        waters = waters.filter(cadastr_number=cadastr_number)

    area = request.GET.get("area")
    if area:
        try:
            waters = waters.filter(area=float(area))
        except ValueError:
            pass

    location = request.GET.get("location")
    if location:
        waters = waters.filter(location__icontains=location)

    destination = request.GET.get("destination")
    if destination:
        waters = waters.filter(destination=destination)

    land = request.GET.get("land")
    if land:
        waters = waters.filter(land=land)

    coordinates = request.GET.get("coordinates")
    if coordinates:
        try:
            waters = waters.filter(coordinates=float(coordinates))
        except ValueError:
            pass

    owner_name = request.GET.get("owner_name")
    if owner_name:
        waters = waters.filter(owner_name__icontains=owner_name)

    rent_start = request.GET.get("rent_start")
    if rent_start:
        try:
            date_start = datetime.strptime(rent_start, '%Y-%m-%d').date()
            waters = waters.filter(rent_start=date_start)
        except ValueError:
            pass

    rent_end = request.GET.get("rent_end ")
    if rent_end:
        try:
            date_end = datetime.strptime(rent_end , '%Y-%m-%d').date()
            waters = waters.filter(rent_end =date_end)
        except ValueError:
            pass

    interest = request.GET.get("interest")
    if interest:
        try:
            waters = waters.filter(interest=float(interest))
        except ValueError:
            pass

    assessment = request.GET.get("assessment")
    if assessment:
        try:
            waters = waters.filter(assessment=float(assessment))
        except ValueError:
            pass

    date_approval = request.GET.get("date_approval")
    if date_approval:
        try:
            date_approval = datetime.strptime(rent_end , '%Y-%m-%d').date()
            waters = waters.filter(date_approval =date_approval)
        except ValueError:
            pass


    for num, plot in enumerate(waters, start=1):
        sheet.append([
            num,
            plot.cadastr_number,
            plot.area,
            plot.location,
            plot.get_destination_display(),
            plot.get_land_display(),
            plot.coordinates,
            plot.owner_name,
            plot.rent_start.strftime('%d.%m.%Y') if plot.rent_start else '',
            plot.rent_end.strftime('%d.%m.%Y') if plot.rent_end else '',
            plot.interest,
            plot.assessment,
            plot.notes,
            plot.pass_number,
            plot.pass_name,
            plot.pass_area,
            plot.pass_volume,
            plot.pass_depth,
            plot.date_approval.strftime('%d.%m.%Y') if plot.date_approval else '',
            plot.pass_developer
        ])
        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = length + 2
    # Відповідь
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=waters.xlsx'
    workbook.save(response)
    return response

def location_autocomplete(request):
    if 'term' in request.GET:
        search_term = request.GET.get('term')
        locations = LandPlot.objects.filter(location__icontains=search_term).values_list('location', flat=True).distinct()
        return JsonResponse(list(locations), safe=False)
    return JsonResponse([], safe=False)

def cadastr_autocomplete(request):
    if 'term' in request.GET:
        search_term = request.GET.get('term')
        cadastr = LandPlot.objects.filter(cadastr_number__icontains=search_term).values_list('cadastr_number', flat=True).distinct()
        return JsonResponse(list(cadastr), safe=False)
    return JsonResponse([], safe=False)

def owner_autocomplete(request):
    if 'term' in request.GET:
        search_term = request.GET.get('term')
        print(f"Search term: {search_term}")
        # Фільтруємо унікальні значення вже на сервері
        qs = LandPlot.objects.filter(owner_name__icontains=search_term).values_list('owner_name', flat=True).distinct()
        return JsonResponse(list(qs), safe=False)
    return JsonResponse([], safe=False)