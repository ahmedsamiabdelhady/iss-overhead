import requests
from datetime import datetime
import smtplib
import time

#get your latitude and longitude from https://www.latlong.net/ .
MY_LAT = 0 # Your latitude
MY_LONG = 0 # Your longitude
my_mail= "your email"
password="password"


def is_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
       return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour= time_now.hour
    if sunset <= hour <= sunrise:
       return True

while True:
    time.sleep(60)
    if is_overhead() and is_dark():
        #write the SMTP and port .
        with smtplib.SMTP(SMTP, port) as connection:
            connection.starttls()
            connection.login(my_mail, password)
            connection.sendmail(
                my_mail,
                my_mail,
                "Supject: Look up!\n\nDon't miss that, the ISS is over your head right now! ."
            )

