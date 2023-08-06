from ..module import Module

try: import requests 
except: print("ModuleWeather: requests module not found!")

class ModuleWeather(Module):

    def __init__(self,  api_key: str, str_format: str="{city}: {data}°",
                        city: str="London", country: str="UK",
                        periodic: float=600.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format
        self.city       = city
        self.country    = country
        self.api_key    = api_key

    def execute(self) -> str:
        loc_url     = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&limit=1&appid={self.api_key}"
        loc_js      = requests.get(loc_url).json()
        lat, lon    = loc_js[0]['lat'], loc_js[0]['lon']
        
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        weather_js  = requests.get(weather_url).json()
        data        = str(weather_js['main']['temp'])

        result = self.str_format
        result = result.replace("{city}", self.city)
        result = result.replace("{data}", data)
        return result

