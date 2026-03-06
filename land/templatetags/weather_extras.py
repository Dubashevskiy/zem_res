from django import template

register = template.Library()

@register.filter
def deg_to_compass(deg):
    try:
        deg = float(deg)
    except (TypeError, ValueError):
        return ''
    dirs = ['Пн', 'Пн-Сх', 'Сх', 'Пд-Сх', 'Пд', 'Пд-Зх', 'Зх', 'Пн-Зх']
    ix = round(deg / 45) % 8
    return dirs[ix]