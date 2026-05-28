import json


class FlightSearchTool:

    def __init__(self, file_path="data/flights.json"):

        self.file_path = file_path

    def load_flights(self):

        with open(self.file_path, "r") as file:
            return json.load(file)

    def search_flights(self, source, destination):

        flights = self.load_flights()

        # CLEAN INPUTS
        source = source.strip().lower()
        destination = destination.strip().lower()

        filtered = []

        for flight in flights:

            flight_from = flight["from"].strip().lower()
            flight_to = flight["to"].strip().lower()

            if (
                flight_from == source
                and flight_to == destination
            ):
                filtered.append(flight)

        # NO ROUTE FOUND
        if not filtered:

            return {
                "status": "error",
                "message": (
                    f"No flights available from "
                    f"{source.title()} to "
                    f"{destination.title()}"
                )
            }

        # CHEAPEST FLIGHT
        cheapest = min(
            filtered,
            key=lambda x: x["price"]
        )

        return {
            "status": "success",
            "selected_flight": cheapest,
            "all_flights": filtered
        }