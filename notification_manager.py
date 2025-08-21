from dotenv import load_dotenv
from twilio.rest import Client
import smtplib
import os
import logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
class NotificationManager:
    """
       Manages sending notifications via SMS and Email.
    """
    def __init__(self):
        self._account_sid = os.getenv("ACCOUNT_SID")
        self._auth_token = os.getenv("AUTH_TOKEN")
        self._app_password = os.getenv("APP_PASSWORD")
        self._smtp_address = os.getenv("SMTP_ADDRESS")
        self.my_email = os.getenv("MY_EMAIL_ADDRESS")
    """
        Sends an SMS message via Twilio.
    """
    def send_sms(self, message: str) -> str:
        client = Client(self._account_sid, self._auth_token)
        client.messages.create(
            body=message,
            from_=os.environ["TWILIO_PHONE_NUMBER"],
            to=os.environ["MY_PHONE_NUMBER"]
        )
        logging.info("SMS sent successfully.")
        return "SMS sent successfully."
    def send_email(self,email:str,message:str) -> None:
        with smtplib.SMTP(self._smtp_address,587) as connection:
            connection.starttls()
            connection.login(self.my_email, self._app_password)
            connection.sendmail(from_addr=self.my_email,to_addrs=email,msg=message)
        logging.info("Email sent successfully.")