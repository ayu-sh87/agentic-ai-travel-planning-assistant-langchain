from  tools.flight_tool import FlightSearchTool
from tools.hotel_tool import HotelRecommendationTool
from tools.places_tool import PlacesDiscoveryTool
from tools.weather_tool import WeatherTool
from tools.budget_tool import BudgetEstimationTool

from utils.helper import create_daywise_plan

class TravelAgent:
    def __init__(self):


        self.flight_tool = FlightSearchTool()
        self.hotel_tool = HotelRecommendationTool()
        self.places_tool = PlacesDiscoveryTool()
        self.weather_tool = WeatherTool()
        self.budget_tool = BudgetEstimationTool()

    def generate_trip_plan(self, source, destination, days):

        flight_data = self.flight_tool.search_flights(
            source,
            destination
        )

        hotel_data = self.hotel_tool.recommend_hotels(destination)

        places_data = self.places_tool.get_places(destination)

        weather_data = self.weather_tool.get_weather(destination)
        if flight_data["status"] == "error":
            return flight_data

        if hotel_data["status"] == "error":
            return hotel_data

        if places_data["status"] == "error":
            return places_data

        selected_flight = flight_data["selected_flight"]
        selected_hotel = hotel_data["best_hotel"]
        selected_places = places_data["top_places"]

        budget = self.budget_tool.estimate_budget(
            selected_flight["price"],
            selected_hotel["price_per_night"],
            days
        )

        itinerary = create_daywise_plan(
            selected_places,
            days
        )

        return {
            "trip_summary": {
                "source": source,
                "destination": destination,
                "days": days
            },
            "flight": selected_flight,
            "hotel": selected_hotel,
            "places": selected_places,
            "weather": weather_data["forecast"][:days],
            "budget": budget,
            "itinerary": itinerary,
            "reasoning": (
                "Selected cheapest flight, highest-rated hotel, "
                "and top-rated attractions."
            )
        }