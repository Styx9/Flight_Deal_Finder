import datetime
import time
import logging
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData, find_cheapest_flight
from notification_manager import NotificationManager

logging.basicConfig(level=logging.INFO)

# Constants
ORIGIN_CITY_IATA = "LON"
SEARCH_DELAY = 2
IATA_DELAY = 1
EMAIL_SUBJECT = "Subject:The Flight Club\n\n"

def build_message(flight: FlightData, include_stops: bool = False) -> str:
    """
    Builds a notification message for the cheapest flight found.
    """
    if include_stops:
        return (
            f"Low Price Alert! Only {flight.price} EUR to fly from "
            f"{flight.origin_city} to {flight.destination_city}, "
            f"from {flight.out_date} to {flight.return_date} "
            f"with {flight.stops} layover(s)."
        )
    return (
        f"Low Price Alert! Only {flight.price} EUR to fly from "
        f"{flight.origin_city} to {flight.destination_city}, "
        f"from {flight.out_date} to {flight.return_date}."
    )


def main() -> None:
    """
    Main script to search for flights and notify customers if cheaper prices are found.
    """
    flight_search = FlightSearch()
    data_manager = DataManager()
    notification_manager = NotificationManager()

    sheet_data = data_manager.get_destination_data()
    users_data = data_manager.get_customer_email()
    customer_email_list = [row["email"] for row in users_data]

    # Update IATA codes if missing
    for row in sheet_data:
        if not row["iataCode"]:
            row["iataCode"] = flight_search.get_iata_code(row["city"])
            time.sleep(IATA_DELAY)

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    one_week_from_today = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    for destination in sheet_data:
        logging.info(f"Searching flights to {destination['city']}...")

        flight_data = flight_search.get_flight_offers(
            ORIGIN_CITY_IATA, destination["iataCode"], tomorrow, one_week_from_today
        )
        cheapest_flight = find_cheapest_flight(flight_data)

        # Try with layovers if no direct flight
        if cheapest_flight.price == "N/A":
            logging.info(f"No direct flights found for {destination['city']}, trying with layovers.")
            stopover_flights = flight_search.get_flight_offers(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                departure_date=tomorrow,
                return_date=one_week_from_today,
                is_direct=False,
            )
            cheapest_flight = find_cheapest_flight(stopover_flights)

            if cheapest_flight.price != "N/A":
                message = build_message(cheapest_flight, include_stops=True)
                #notification_manager.send_sms(message)
                for customer in customer_email_list:
                    notification_manager.send_email(customer, EMAIL_SUBJECT + message)

        elif destination["lowestPrice"] > float(cheapest_flight.price):
            message = build_message(cheapest_flight)
            #notification_manager.send_sms(message)
            for customer in customer_email_list:
                notification_manager.send_email(customer, EMAIL_SUBJECT + message)

        time.sleep(SEARCH_DELAY)


if __name__ == "__main__":
    main()
