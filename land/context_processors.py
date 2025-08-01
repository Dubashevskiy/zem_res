import requests
from datetime import datetime

def weather_context(request):
    city = 'Жашків'  # або можна отримувати динамічно
    api_key = '8d2f86ddab8282673d32ced9d3f19ebd'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ua'
    response = requests.get(url)
    data = response.json()

    weather = {}
    if response.status_code == 200:
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'clouds': data['clouds']['all'],
        }
    else:
        weather['error'] = 'Погода недоступна'

    return {'weather': weather}