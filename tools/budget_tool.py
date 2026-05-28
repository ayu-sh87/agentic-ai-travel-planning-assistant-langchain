class BudgetEstimationTool:

    def estimate_budget(self, flight_price, hotel_price, days):

        hotel_total = hotel_price * days

        food_transport = days * 1500

        total_cost = flight_price + hotel_total + food_transport

        return {
            "flight_cost": flight_price,
            "hotel_cost": hotel_total,
            "food_and_transport": food_transport,
            "total_cost": total_cost
        }