import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()
# Получаем API ключ для доступа к OpenWeatherMap
api_key = os.getenv("API_KEY")

def get_current_weather(city: str=None, lat: float=None, lon: float=None) -> dict:
    if city:
        print(f"Получаем погоду для города: {city}")
        return

    if lat is not None and lon is not None:
        print(f"Получаем погоду для координат: {lat}, {lon}")
        return get_weather_by_coordinates(lat, lon)


def get_coordinates(city: str) -> tuple:
    """
    Получает координаты (широту и долготу) города по его названию.
    
    Аргументы:
        city (str): Название города
    
    Возвращает:
        tuple: Кортеж (широта, долгота) или None при ошибке
    """
    # Формируем URL для запроса к API геолокации OpenWeatherMap
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Возвращаем широту и долготу первого результата
            return data[0]["lat"], data[0]["lon"]
    else:
        print(f"Ошибка при получении данных о погоде: {response.status_code}")
        return None

def get_weather_by_coordinates(latitude: float, longitude: float) -> dict:
    """
    Получает данные о погоде по координатам (широта и долгота).
    
    Аргументы:
        latitude (float): Широта координат
        longitude (float): Долгота координат
    
    Возвращает:
        dict: Словарь с данными о погоде или None при ошибке
    """
    # Формируем URL для запроса текущей погоды
    # units=metric - результаты в метрических единицах (Цельсий, м/с)
    # lang=ru - ответ на русском языке
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении данных о погоде: {response.status_code}")
        return None



if __name__ == "__main__":
    city = input("Введите название города:")
    coordinates = get_coordinates(city)
    if coordinates:
        lat, lon = coordinates
        weather = get_weather_by_coordinates(lat, lon)
        if weather:
            print(f"Погода в {weather['name']}: {weather['main']['temp']}°C, {weather['weather'][0]['description']}")
    else:
        print("Не удалось получить данные о погоде.")
