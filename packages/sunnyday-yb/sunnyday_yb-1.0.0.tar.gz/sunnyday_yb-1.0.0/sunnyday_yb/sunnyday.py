import requests


class Weather:
    """Creates a Weather object getting an apikey and
    either a city name or lat and lon coordinates as input

    Package us example:

    # apikey used in the example is not guaranteed to work
    # Get your own apikey from https://openweathermap.org and
    # wait a couple of hours for the apikey to be activated

    # Create a Weather object using a city name
    >>> weather1= Weather(apikey="ebfd0104edd83ecb26bfa9992a41a699", city="Seattle")

    # Create a Weather object sing latitude and longitude coordinates
    >>> weather2 = Weather(apikey="ebfd0104edd83ecb26bfa9992a41a699", lat=41.1, lon=4.1)

    # Get complete weather data for the next 12 hours
    >>> weather1.next_12h()

    # Get simplified weather data for the next 12 hours
    >>> weather1.next_12h_simplified()
    """

    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city or lat and lon arguments")

        if self.data['cod'] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temp, and sky condition every 3 hours for the next 12 hours as a list of tuples
        """
        simple_data = []

        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))

        return simple_data
