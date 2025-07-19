import requests
from bs4 import BeautifulSoup
import time

def build_search_url(city):
    base_url = "https://www.accuweather.com/en/search-locations"
    params = {"query": city}
    response = requests.get(base_url, params=params)
    return response.url

def get_city_weather_url(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    first_result = soup.find("a", class_="locations-list-content")
    if first_result and first_result.has_attr("href"):
        return "https://www.accuweather.com" + first_result["href"]
    else:
        raise ValueError("City weather URL not found.")

def fetch_weather_page(weather_url):
    response = requests.get(weather_url)
    return response.text

def parse_weather(html):
    soup = BeautifulSoup(html, "html.parser")
    weather = {}
    temp = soup.find("div", class_="temp")
    if temp:
        weather["temperature"] = temp.text.strip()
    else:
        weather["temperature"] = "N/A"

    # Fix: class_ is not needed for a tag, attrs={'class': ...} is, but for just an attribute, use id or attrs
    # Also, .text is a property, not a function
    condition = soup.find("span", attrs={"class": "phrase"})
    if condition:
        weather["condition"] = condition.text.strip()
    else:
        weather["condition"] = "N/A"

    wind = soup.find("div", class_="wind")
    if wind:
        weather["wind"] = wind.text.strip()
    else:
        weather["wind"] = "N/A"

    humidity = soup.find("div", class_="humidity")
    if humidity:
        weather["humidity"] = humidity.text.strip()
    else:
        weather["humidity"] = "N/A"

    return weather

def print_weather(city, weather):
    print(f"Weather for {city}:")
    print(f"Temperature: {weather['temperature']}")
    print(f"Condition: {weather['condition']}")
    print(f"Wind: {weather['wind']}")
    print(f"Humidity: {weather['humidity']}")

def crawl_accuweather(city):
    print(f"Searching for city: {city}")
    search_url = build_search_url(city)
    print(f"Search URL: {search_url}")

    try:
        weather_url = get_city_weather_url(search_url)
        print(f"Weather URL: {weather_url}")

        html = fetch_weather_page(weather_url)
        weather = parse_weather(html)
        print_weather(city, weather)
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")

if __name__ == "__main__":
    cities = ["New York", "London", "Tokyo", "Sydney"]
    for city in cities:
        crawl_accuweather(city)
        time.sleep(2)
