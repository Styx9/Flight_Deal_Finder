import logging

logging.basicConfig(level=logging.INFO)
class FlightData:
    """
        Stores details about a flight.
    """

    def __init__(
            self,
            price: float | str,
            origin_city: str,
            destination_city: str,
            out_date: str,
            return_date: str,
            stops: int | str
    ) -> None:
        self.price = price
        self.origin_city = origin_city
        self.destination_city = destination_city
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops
def find_cheapest_flight(flight_data: dict | None) -> FlightData:
    """
    Finds the cheapest flight from API response data.

    :param flight_data: API response containing flights.
    :return: FlightData instance of cheapest flight.
    """
    if not flight_data or not flight_data.get("data"):
        logging.warning("No flights found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    cheapest_flight: FlightData | None = None
    lowest_price = float("inf")

    for flight in flight_data["data"]:
        price = float(flight["price"]["grandTotal"])
        segments = flight["itineraries"][0]["segments"]
        nr_stops = len(segments) - 1

        if price < lowest_price:
            lowest_price = price
            origin = segments[0]["departure"]["iataCode"]
            destination = segments[-1]["arrival"]["iataCode"]
            out_date = segments[0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["arrival"]["at"].split("T")[0]

            cheapest_flight = FlightData(
                lowest_price, origin, destination, out_date, return_date, nr_stops
            )

    logging.info(f"Cheapest flight: {cheapest_flight.price} EUR from {cheapest_flight.origin_city} to {cheapest_flight.destination_city}")
    return cheapest_flight