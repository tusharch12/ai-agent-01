import requests

def whether_api(city_name):
    
    response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json')
    latitude = response.json()['results'][0]['latitude']
    longitude = response.json()['results'][0]['longitude']

    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true')
    
    return response.json()['current_weather']


# city_name = input('Enter the city name: ')

# print('Whether API {city_name}', whether_api(city_name))