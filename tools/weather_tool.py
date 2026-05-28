import requests


class WeatherTool:

    def __init__(self):

        # CITY COORDINATES
        self.city_coordinates = {

            "goa": (15.2993, 74.1240),
            "delhi": (28.6139, 77.2090),
            "mumbai": (19.0760, 72.8777),
            "bangalore": (12.9716, 77.5946),
            "kolkata": (22.5726, 88.3639),
            "hyderabad": (17.3850, 78.4867),
            "jaipur": (26.9124, 75.7873),
            "chennai": (13.0827, 80.2707)

        }

    def get_weather(self, city):

        city = city.strip().lower()

        # CHECK CITY EXISTS
        if city not in self.city_coordinates:

            return {
                "status": "error",
                "message": f"Weather unavailable for {city.title()}"
            }

        latitude, longitude = self.city_coordinates[city]

        # OPEN-METEO API
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&"
            f"longitude={longitude}&"
            f"daily=temperature_2m_max&"
            f"timezone=auto"
        )

        try:

            response = requests.get(url)

            data = response.json()

            weather_data = []

            dates = data["daily"]["time"]

            temperatures = data["daily"]["temperature_2m_max"]

            for date, temp in zip(dates, temperatures):

                weather_data.append({

                    "date": date,
                    "temperature": temp

                })

            return {

                "status": "success",
                "forecast": weather_data

            }

        except Exception as error:

            return {

                "status": "error",
                "message": str(error)

            }