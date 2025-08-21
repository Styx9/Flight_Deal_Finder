✈️ Flight Club – Cheap Flight Finder

This project helps you track cheap flight deals using the Amadeus API and notifies you when prices drop below a set threshold. Notifications are sent via Twilio SMS and Email (SMTP). Costumer emails are gathered via a Google Form that is connected to a Google Sheet.

📌 Features

Fetches IATA codes for cities automatically.

Searches flight offers (direct or with layovers).

Finds and stores the cheapest available flight.

Sends alerts via SMS and Email to subscribed users.

Integrates with Google Sheets (Sheety API) to manage destinations and users.

⚙️ Tech Stack

Python 3

Amadeus API (Flight data)

Twilio API (SMS)

SMTP (Email)

Sheety API (Google Sheets integration)

dotenv for environment variables
