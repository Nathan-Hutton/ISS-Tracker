import requests
import smtplib
import os
import math
from dotenv import load_dotenv
from datetime import datetime

MY_LONG = -111.093735
MY_LAT = 39.320980
def iss_overhead():
    iss_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_response.raise_for_status()

    longitude = iss_response.json()["iss_position"]['longitude']
    latitude = iss_response.json()["iss_position"]['latitude']
    iss_position = (float(longitude), float(latitude))
    print(iss_position)
    if math.isclose(iss_position[0], MY_LONG, rel_tol=5) and math.isclose(iss_position[1], MY_LAT, rel_tol=5):
        return True
    return False

def is_night():
    parameters = {
        'lat': MY_LAT,
        'long': MY_LONG,
        'formatted': 0}
    sun_response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()

    sunrise = int(sun_data['results']['sunrise'].split("T")[1][0:2])
    sunset = int(sun_data['results']['sunset'].split("T")[1][0:2])
    time_now_hour = datetime.now().hour
    if sunset <= time_now_hour or time_now_hour <= sunrise:
        return True
    return False

load_dotenv('/Users/natha/PycharmProjects/info.env')

my_email = os.getenv('EMAIL')
recipient_email = os.getenv('TARGET_EMAIL')
my_password = os.getenv('EMAIL_PASSWORD')
generated_password = os.getenv('EMAIL_GENERATED_PASSWORD')

with smtplib.SMTP(os.getenv('SMTP'), int(os.getenv('PORT'))) as connection:
    connection.starttls()
    connection.login(user=my_email, password=generated_password)
    if is_night() and iss_overhead():
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient_email,
            msg=f"The ISS is overhead")
