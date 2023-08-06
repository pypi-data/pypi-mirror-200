import requests


class Weather:
    """
    Creates a Weather object getting a city or coordinates (latitude and longitude) and gives back weather information.
    Gives the weather information for 3 hours of weather for 5 days.
    
    Notice:
    
    # Create your own api key from openweathermap
    # The default api key is might not work
    # Wait for a couple of hours as it takes time for the api key to activate
    
    Installation:
    $ pip install weatherpy2
    
    Use Case:
    
    #Import statement
    >>> import weatherpy2 as wp2
    
    #With city
    >>> weather_obj = wp2.Weather(city_name='atlanta')
    
    #With latitude and longitude
    >>> weather_obj = wp2.Weather(lat=41, lon=4.1)
    
    #Without default api key
    >>> weather_obj = wp2.Weather(api_key="4bf8b4b38210efcad266de093a25a692", city_name='atlanta')
    
    #Returns complete weather data
    >>> weather_obj.weather_data()
    
    #Returns simplified weather data
    >>> weather_obj.weather_simple()
    """
    def __init__(self, api_key="4bf8b4b38210efcad266de093a25a692", city_name=None, lat=None, lon=None, units="metric"):
        if city_name and lat and lon:
            raise ValueError("City and coordinates are provided together. Provide only one of those arguments.")
        else:

            if city_name:
                url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units={units}"
            elif lat and lon:
                url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={units}"
            else:
                raise TypeError("Invalid Arguments: City or Coordinates are missing.")
            
        self.request = requests.get(url, timeout=20)
        self.data = self.request.json()
        
        if self.data["cod"] != "200":
            raise ValueError(self.data['message'])
    
    def weather_data(self):
        return self.data["list"]
    
    def weather_simple(self):
        simple_data = []
        for index in self.data["list"]:
            simple_data.append((index["dt_txt"], index["main"]["temp"], index["weather"][0]["description"]))
        return simple_data