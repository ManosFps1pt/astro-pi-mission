""""
                SPEED ESTIMATION OF ISS
    IERCSLG of 3rd GYMNASIUM OF IERAPETRA CRETE GREECE
    
To estimate the speed of ISS we use geographic coordinates to measure the distance in kms between two points (A, B) on the
surface of the earth, within time intervals of 1 second, i.e.
we take the position of ISS "now" and retake its position after 1 sec.
Then we devide the distance travelled by the time interval to calculate
the speed, in our case since time interval equals 1 sec, speed equals the travalled distance.

In order calculate the distance between any two points we use the Harvesine formula as explained in: https://www.youtube.com/watch?v=HaGj0DjX8W8.
We use time intervals of 1 second because according to our experiments it results to a better estimation, however
our program is general enough to allow any time interval by changing appropriately the value of "wait_time" variable.

We collect plenty such pair of points with each point pair resulting in a different speed estimation.
As the final speed estimation we take the median of the collected values.

In the mean time we collect various sensor values such as temprature, humidity, pressure, latitude, longitude etc.
which are saved in a .csv file, while intermediate results are kept in the output.txt file. The fianl result of speed
estimation is saved in the result.txt file.

"""

import os
import sys

libPath = 'C:/Users/Admin/AppData/Roaming/Python/Python310/site-packages/astro_pi_replay'
if not libPath in sys.path: sys.path.append(libPath)
import pandas as pd
from math import acos, sin, cos
from datetime import datetime
from datetime import timedelta
from pathlib import Path
#import matplotlib.pyplot as plt
import numpy as np
#from picamzero import Camera
from picamera import PiCamera
from orbit import ISS
from time import sleep
from sense_hat import SenseHat
import csv

# constant variables for storing the path of every file we create
BASE_FOLDER = Path(__file__).parent.resolve()
DATA_FILE_1_PATH = BASE_FOLDER / "result.txt"
DATA_FILE_2_PATH = BASE_FOLDER / "log_file.txt"
DATA_FILE_3_PATH = BASE_FOLDER / "data.csv"

# we open file 2
DATA_FILE_2 = open(DATA_FILE_2_PATH, "w", buffering=1)

# we create a SenseHat, ISS and PiCamera objects
sense = SenseHat()
iss = ISS()
cam = PiCamera()


def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure", "Compass")
        writer.writerow(header)


def add_csv_data(data_file, data) -> None:
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def convertAngle(angle):
    # Convert a `skyfield` Angle to an Exif-appropriate
    # representation (positive rationals)
    # e.g. 98° 34' 58.7 to "98/1,34/1,587/10"
    # Return a tuple containing a Boolean and the converted angle,
    # with the Boolean indicating if the angle is negative
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture_image(iss, camera, base_folder, image):
    # Use `camera` to capture an `image` file with lat/long Exif data
    point = iss.coordinates()
    # Convert the latitude and longitude to Exif-appropriate
    # representations
    south, exif_latitude = convertAngle(point.latitude)
    west, exif_longitude = convertAngle(point.longitude)
    # Set the Exif tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
    
    # Capture the image
    camera.capture(f"{base_folder}\\{image}.jpg")
    

earth_rad: float = 3440.1  #miles
earth_rad = 6378  #kms
wait_time = 5  #seconds
velocityList = []

# Create a variable to store the start time
start_time = datetime.now()
# Create a variable to store the current time
# (these will be almost the same at the start)
now_time = datetime.now()
i = 1
create_csv_file(DATA_FILE_3_PATH)
while (now_time < start_time + timedelta(minutes=.2)):
    try:
        DATA_FILE_2.write("================================================================================\n")
        DATA_FILE_2.write(f"Iteration = {i}\n")
        location = ISS().coordinates()

        radLongA = location.longitude.radians
        radLatA = location.latitude.radians
        degLongA = location.longitude.degrees
        degLatA = location.latitude.degrees
        elevA = location.elevation.km

        DATA_FILE_2.write(f'LongitudeA degrees = {degLongA}\n')
        DATA_FILE_2.write(f'LatitudeA degrees = {degLatA}\n')
        
        humidity = round(sense.humidity, 1)
        temperature = round(sense.temperature, 1)
        pressure = round(sense.pressure, 1)
        compass = round(sense.compass, 1)
        data = i, datetime.now(), degLatA, degLongA, temperature, humidity, pressure, compass

        add_csv_data(DATA_FILE_3_PATH, data)
        sleep(wait_time)

        location = ISS().coordinates()
        DATA_FILE_2.write(f'LongitudeB degress = {location.longitude.degrees}\n')
        DATA_FILE_2.write(f'LatitudeB degrees = {location.latitude.degrees}\n')

        radLongB = location.longitude.radians
        radLatB = location.latitude.radians
        elevB = location.elevation.km
        DATA_FILE_2.write(f"Altitude = {location.elevation.km:.2f} km\n")
        distance = (earth_rad + location.elevation.km) * acos((sin(radLatA) * sin(radLatB)) +
                                                              cos(radLatA) * cos(radLatB) * cos(radLongA - radLongB))
        distance = distance + (1670 / 3600) * wait_time + abs(elevB - elevA)
        velocity = distance / wait_time
        DATA_FILE_2.write("distance =  %2.2f km, velocity =  %.5f km/sec latB - latA = %.5f\n" % (
            distance, velocity, (radLatB - radLatA)))
        velocityList.append(velocity)
        
        humidity = round(sense.humidity, 1)
        temperature = round(sense.temperature, 1)
        pressure = round(sense.pressure, 1)
        compass = round(sense.compass, 1)
        data = i, datetime.now(), degLatA, degLongA, temperature, humidity, pressure, compass
        add_csv_data(DATA_FILE_3_PATH, data)
        if i < 40:
            DATA_FILE_2.write(f"photo: image{i}.jpg\n")
            capture_image(iss, cam, BASE_FOLDER, f"image {i}")
        i += 1
        DATA_FILE_2.write("================================================================================\n")
        now_time = datetime.now()
    except Exception as e:
        msg = f"exception occured!!!!! ({repr(e)})\n"
        print(msg)
        DATA_FILE_2.write(msg)
        quit()
    

velocityList.sort()
estimate_kmps = velocityList[len(velocityList) // 2]
print(f'Estimates Velocity = {estimate_kmps:.4f} km/sec')

with open(DATA_FILE_1_PATH, "w", buffering=1) as file1:
    file1.write(f"{estimate_kmps:.4f}\n")

print("data written to", DATA_FILE_1_PATH)
DATA_FILE_2.write(f"execution time {datetime.now() - start_time}\n")
DATA_FILE_2.close()
