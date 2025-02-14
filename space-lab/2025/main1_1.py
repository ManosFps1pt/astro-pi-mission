import os
import sys
libPath = 'C:/Users/Admin/AppData/Roaming/Python/Python310/site-packages/astro_pi_replay'
if not libPath in sys.path: sys.path.append(libPath)
import pandas as pd
import math
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

base_folder = Path(__file__).parent.resolve()
data_file1 = base_folder / "result.txt"
data_file2 = base_folder / "log_file.txt"
data_file3 = base_folder / "data.csv"
print(type(base_folder))
file2 = open(data_file2, "w", buffering=1)
sense = SenseHat()

def covert_degrees_radians(degrees):
    return degrees*math.pi/180

def get_gps_coordinates(iss):
    point = iss.coordinates()
    return (point.latitude.signed_dms(), point.longitude.signed_dms())

def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure", "Compass")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
earth_rad = 3440.1 #miles
earth_rad = 6378 #kms
pythLst = [0]
harvLst = [0]
wait_time = 5 #seconds
velocityList =[]
iss = ISS()
cam = PiCamera()
#for i in range(len(data_set)-1):
# Create a variable to store the start time
start_time = datetime.now()
# Create a variable to store the current time
# (these will be almost the same at the start)
now_time = datetime.now()
i = 1
create_csv_file(data_file3)
while (now_time < start_time + timedelta(minutes=.2)):
    try:
        #cam.take_photo(imgStr, gps_coordinates=get_gps_coordinates(iss))
        if i < 40:
            imgStr = str(base_folder) + "/" f"image{i}.jpg"
            cam.capture(imgStr)

        file2.write("================================================================================\n")
        file2.write(f"Iteration = {i}\n")
        location = ISS().coordinates()


        radLongA = location.longitude.radians
        radLatA = location.latitude.radians
        degLongA = location.longitude.degrees
        degLatA = location.latitude.degrees
        elevA = location.elevation.km

        file2.write(f'LongitudeA degrees = {degLongA}\n')
        file2.write(f'LatitudeA degrees = {degLatA}\n')
        
        #Taking measurements from the sensors
        humidity = round(sense.humidity, 1)
        temperature = round(sense.temperature, 1)
        pressure = round(sense.pressure, 1)
        compass = round(sense.compass, 1)
        data = i, datetime.now(), degLatA, degLongA, temperature, humidity, pressure, compass
        add_csv_data(data_file3, data)
        sleep(wait_time)
        
        location = ISS().coordinates()
        file2.write(f'LongitudeB degress = {location.longitude.degrees}\n')
        file2.write(f'LatitudeB degrees = {location.latitude.degrees}\n')

        radLongB = location.longitude.radians
        radLatB = location.latitude.radians
        elevB = location.elevation.km
        file2.write(f"Altitude = {location.elevation.km:.2f} km\n")
        distance = (earth_rad + location.elevation.km)*math.acos((math.sin(radLatA)*math.sin(radLatB))+
                                    math.cos(radLatA)*math.cos(radLatB)*math.cos(radLongA-radLongB))
        distance = distance + (1670/3600) * wait_time  + abs(elevB-elevA)
        velocity = distance / wait_time
        file2.write("distance =  %2.2f km, velocity =  %.5f km/sec latB - latA = %.5f\n" %(distance, velocity, (radLatB - radLatA)))
        velocityList.append(velocity)
        file2.write("================================================================================\n")
        i += 1
        now_time = datetime.now()
    except Exception as e:
        msg = f"exception occured!!!!! ({e})\n"
        print(msg)
        file2.write(msg)
        quit()

        

velocityList.sort()
estimate_kmps = velocityList[len(velocityList)//2]
print(f'Estimates Velocity = {estimate_kmps:.5f} km/sec')

with open(data_file1, "w", buffering=1) as file1:
    file1.write(f"{estimate_kmps:.4f}\n")

print("data written to", data_file1)
file2.write(f"execution time {datetime.now()-start_time}\n")
file2.close()