import json


class HotelRecommendationTool:

    def __init__(self, file_path="data/hotels.json"):
        self.file_path = file_path

    def load_hotels(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def recommend_hotels(self, city):

        hotels = self.load_hotels()

        filtered = [
            hotel for hotel in hotels
            if hotel["city"].lower() == city.lower()
        ]

        if not filtered:
            return {
                "status": "error",
                "message": "No hotels found"
            }

        ranked = sorted(
            filtered,
            key=lambda x: (-x["stars"], x["price_per_night"])
        )

        return {
            "status": "success",
            "recommended_hotels": ranked[:5],
            "best_hotel": ranked[0]
        }