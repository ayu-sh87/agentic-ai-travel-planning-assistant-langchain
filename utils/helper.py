from datetime import datetime


def format_currency(amount):
    return f"₹{amount:,}"


def create_daywise_plan(places, days):

    itinerary = {}

    index = 0

    for day in range(1, days + 1):

        daily_places = []

        for _ in range(2):
            if index < len(places):
                daily_places.append(places[index]["name"])
                index += 1

        itinerary[f"Day {day}"] = daily_places

    return itinerary