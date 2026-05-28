import json


class PlacesDiscoveryTool:

    def __init__(self, file_path="data/places.json"):
        self.file_path = file_path

    def load_places(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get_places(self, city):

        places = self.load_places()

        filtered = [
            place for place in places
            if place["city"].lower() == city.lower()
        ]

        if not filtered:
            return {
                "status": "error",
                "message": "No places found"
            }

        ranked = sorted(
            filtered,
            key=lambda x: x["rating"],
            reverse=True
        )

        return {
            "status": "success",
            "top_places": ranked[:5]
        }